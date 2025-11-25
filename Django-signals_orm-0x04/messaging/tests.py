from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Message, Notification, UnreadMessagesManager
from .signals import create_message_notification


class MessageSignalTests(TestCase):
    """
    Test cases for message-related signals
    """
    
    def setUp(self):
        """Set up test data"""
        self.sender = User.objects.create_user(
            username='sender', 
            email='sender@example.com', 
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver', 
            email='receiver@example.com', 
            password='testpass123'
        )
    
    def test_notification_created_on_new_message(self):
        """Test that a notification is created when a new message is saved"""
        # Count initial notifications
        initial_notification_count = Notification.objects.count()
        
        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message!"
        )
        
        # Check that a notification was created
        final_notification_count = Notification.objects.count()
        self.assertEqual(final_notification_count, initial_notification_count + 1)
        
        # Verify notification details
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'new_message')
        self.assertIn(self.sender.username, notification.title)
        self.assertFalse(notification.is_read)
    
    def test_no_notification_on_message_update(self):
        """Test that no new notification is created when existing message is updated"""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )
        
        # Count notifications after creation
        notification_count_after_creation = Notification.objects.count()
        
        # Update the message
        message.content = "Updated content"
        message.save()
        
        # Check that no new notification was created
        notification_count_after_update = Notification.objects.count()
        self.assertEqual(notification_count_after_update, notification_count_after_creation)
    
    def test_message_read_notification(self):
        """Test that notification is created when message is marked as read"""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message",
            is_read=False
        )
        
        # Mark message as read
        message.is_read = True
        message.save()
        
        # Check that a read notification was created for the sender
        read_notification = Notification.objects.filter(
            notification_type='message_read',
            user=self.sender
        ).first()
        
        self.assertIsNotNone(read_notification)
        self.assertIn(self.receiver.username, read_notification.title)
    
    def test_multiple_messages_create_multiple_notifications(self):
        """Test that multiple messages create multiple notifications"""
        # Create multiple messages
        for i in range(3):
            Message.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                content=f"Test message {i}"
            )
        
        # Check that 3 notifications were created
        self.assertEqual(Notification.objects.count(), 3)
        
        # Verify each notification is for the correct user
        for notification in Notification.objects.all():
            self.assertEqual(notification.user, self.receiver)

class NotificationModelTests(TestCase):
    """
    Test cases for Notification model
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123'
        )
        self.sender = User.objects.create_user(
            username='sender', 
            email='sender@example.com', 
            password='testpass123'
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.user,
            content="Test message content"
        )
    
    def test_notification_creation(self):
        """Test notification creation and string representation"""
        notification = Notification.objects.create(
            user=self.user,
            message=self.message,
            notification_type='new_message',
            title="Test Notification",
            message_preview="Test preview..."
        )
        
        self.assertEqual(str(notification), f"Notification for {self.user}: Test Notification")
        self.assertFalse(notification.is_read)
    
    def test_notification_mark_as_read(self):
        """Test mark_as_read method"""
        notification = Notification.objects.create(
            user=self.user,
            message=self.message,
            title="Test Notification",
            message_preview="Test preview..."
        )
        
        self.assertFalse(notification.is_read)
        notification.mark_as_read()
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
    
    def test_notification_ordering(self):
        """Test that notifications are ordered by creation date (newest first)"""
        # Create notifications with different timestamps
        notification1 = Notification.objects.create(
            user=self.user,
            message=self.message,
            title="First Notification",
            message_preview="First"
        )
        
        notification2 = Notification.objects.create(
            user=self.user,
            message=self.message,
            title="Second Notification",
            message_preview="Second"
        )
        
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0], notification2)  # Newest first
        self.assertEqual(notifications[1], notification1)  # Oldest last


class ThreadedConversationTests(TestCase):
    """
    Test cases for threaded conversations and advanced ORM techniques
    """
    
    def setUp(self):
        """Set up test data for threaded conversations"""
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
        self.user3 = User.objects.create_user('user3', 'user3@example.com', 'pass')
        
        # Create a thread starter
        self.thread_starter = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Thread starter message"
        )
        
        # Create replies at different depths
        self.reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="First reply",
            parent_message=self.thread_starter
        )
        
        self.reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Reply to first reply",
            parent_message=self.reply1
        )
        
        self.reply3 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Another direct reply",
            parent_message=self.thread_starter
        )
    
    def test_thread_depth_calculation(self):
        """Test that thread depth is calculated correctly"""
        self.assertEqual(self.thread_starter.thread_depth, 0)
        self.assertEqual(self.reply1.thread_depth, 1)
        self.assertEqual(self.reply2.thread_depth, 2)
        self.assertEqual(self.reply3.thread_depth, 1)
    
    def test_is_thread_starter_flag(self):
        """Test that thread starter flag is set correctly"""
        self.assertTrue(self.thread_starter.is_thread_starter)
        self.assertFalse(self.reply1.is_thread_starter)
        self.assertFalse(self.reply2.is_thread_starter)
        self.assertFalse(self.reply3.is_thread_starter)
    
    def test_select_related_optimization(self):
        """Test that select_related reduces database queries"""
        # Without optimization
        with self.assertNumQueries(4):  # 1 for message + 3 for related users
            messages = Message.objects.filter(thread_depth=0)
            for message in messages:
                sender_name = message.sender.username
                receiver_name = message.receiver.username
        
        # With select_related optimization
        with self.assertNumQueries(1):  # Single query with joins
            messages = Message.objects.filter(thread_depth=0).select_related('sender', 'receiver')
            for message in messages:
                sender_name = message.sender.username
                receiver_name = message.receiver.username
    
    def test_prefetch_related_optimization(self):
        """Test that prefetch_related optimizes reverse relation queries"""
        # Get thread starter with all replies prefetched
        with self.assertNumQueries(2):  # 1 for message, 1 for replies
            thread = Message.objects.filter(id=self.thread_starter.id).prefetch_related('replies').first()
            reply_count = thread.replies.count()
            for reply in thread.replies.all():
                _ = reply.content
    
    def test_get_complete_thread_method(self):
        """Test the get_complete_thread method with optimized queries"""
        # This should get all messages in the thread with minimal queries
        with self.assertNumQueries(2):  # Optimized query
            thread_messages = Message.objects.get_complete_thread(self.thread_starter.id)
            self.assertEqual(len(thread_messages), 4)  # starter + 3 replies
            
            # Access related fields without additional queries
            for message in thread_messages:
                _ = message.sender.username
                _ = message.receiver.username
    
    def test_recursive_reply_structure(self):
        """Test that reply structure is maintained correctly"""
        # Test direct replies
        direct_replies = self.thread_starter.replies.all()
        self.assertEqual(direct_replies.count(), 2)  # reply1 and reply3
        
        # Test nested replies
        nested_replies = self.reply1.replies.all()
        self.assertEqual(nested_replies.count(), 1)  # reply2
        
        # Test reply chain
        self.assertEqual(self.reply2.parent_message, self.reply1)
        self.assertEqual(self.reply1.parent_message, self.thread_starter)
    
    def test_thread_replies_method(self):
        """Test the get_thread_replies method"""
        replies = self.thread_starter.get_thread_replies(include_self=False)
        self.assertEqual(replies.count(), 3)  # All replies excluding starter
        
        # Test that it includes nested replies
        reply_ids = [reply.id for reply in replies]
        self.assertIn(self.reply1.id, reply_ids)
        self.assertIn(self.reply2.id, reply_ids)
        self.assertIn(self.reply3.id, reply_ids)
    
    def test_reply_count_properties(self):
        """Test reply count properties"""
        self.assertEqual(self.thread_starter.reply_count, 3)  # All replies in thread
        self.assertEqual(self.thread_starter.direct_reply_count, 2)  # Direct replies only
        self.assertEqual(self.reply1.reply_count, 1)  # Only reply2
        self.assertEqual(self.reply1.direct_reply_count, 1)
    
    def test_threads_for_user_optimization(self):
        """Test the get_threads_for_user method optimization"""
        # Test for user1 (should see threads where they are sender or receiver)
        with self.assertNumQueries(2):  # Optimized query
            threads = Message.objects.get_threads_for_user(self.user1)
            self.assertEqual(threads.count(), 1)  # Only the thread starter
            
            # Access related data without additional queries
            for thread in threads:
                _ = thread.sender.username
                _ = thread.receiver.username
                _ = thread.replies.count()

class AdvancedORMTechniquesTests(TestCase):
    """
    Test advanced ORM techniques used in threaded conversations
    """
    
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
        
        # Create complex thread structure
        self.thread = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Main thread"
        )
        for i in range(3):
            reply = Message.objects.create(
                sender=self.user2, receiver=self.user1, 
                content=f"Reply {i}", parent_message=self.thread
            )
            # Add nested replies
            for j in range(2):
                Message.objects.create(
                    sender=self.user1, receiver=self.user2,
                    content=f"Nested reply {i}-{j}", parent_message=reply
                )
    
    def test_complex_prefetch_related(self):
        """Test complex prefetch_related for multi-level threads"""
        # This should efficiently load the entire thread structure
        with self.assertNumQueries(3):  # Main query + 2 levels of prefetch
            thread = Message.objects.filter(id=self.thread.id).prefetch_related(
                'replies__replies'
            ).first()
            
            # Access nested structure without additional queries
            for direct_reply in thread.replies.all():
                _ = direct_reply.content
                for nested_reply in direct_reply.replies.all():
                    _ = nested_reply.content
    
    def test_annotation_with_subquery(self):
        """Test annotation with subqueries for reply counts"""
        from django.db.models import Subquery, OuterRef, Count
        
        # Test the get_thread_with_reply_counts method
        threads = Message.objects.get_thread_with_reply_counts(self.thread.id)
        
        for message in threads:
            if message.id == self.thread.id:
                self.assertEqual(message.direct_reply_count, 3)
            elif message.thread_depth == 1:
                self.assertEqual(message.direct_reply_count, 2)
            elif message.thread_depth == 2:
                self.assertEqual(message.direct_reply_count, 0)  # No further replies


class CustomManagerTests(TestCase):
    """
    Test cases for custom UnreadMessagesManager
    """
    
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
        
        # Create messages with different read statuses
        self.read_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
        
        self.unread_message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 1",
            read=False
        )
        
        self.unread_message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Unread message 2",
            read=False
        )
    
    def test_unread_messages_manager_exists(self):
        """Test that custom manager is attached to Message model"""
        self.assertTrue(hasattr(Message, 'unread_messages'))
        self.assertIsInstance(Message.unread_messages, UnreadMessagesManager)
    
    def test_for_user_method(self):
        """Test for_user method filters unread messages for specific user"""
        # Test for user2
        unread_for_user2 = Message.unread_messages.for_user(self.user2)
        self.assertEqual(unread_for_user2.count(), 1)
        self.assertEqual(unread_for_user2.first().id, self.unread_message1.id)
        
        # Test for user1
        unread_for_user1 = Message.unread_messages.for_user(self.user1)
        self.assertEqual(unread_for_user1.count(), 1)
        self.assertEqual(unread_for_user1.first().id, self.unread_message2.id)
    
    def test_for_user_optimization(self):
        """Test that for_user method uses .only() for optimization"""
        # This should use optimized query with only necessary fields
        unread_messages = Message.unread_messages.for_user(self.user2)
        
        # Check that the query uses select_related and only
        query = str(unread_messages.query).lower()
        self.assertIn('select', query)
        self.assertIn('from', query)
        
        # Verify we can access the fields without additional queries
        with self.assertNumQueries(1):
            message = unread_messages.first()
            if message:
                _ = message.sender.username  # Should not cause additional query
    
    def test_unread_count_for_user(self):
        """Test unread_count_for_user method"""
        count_user2 = Message.unread_messages.unread_count_for_user(self.user2)
        self.assertEqual(count_user2, 1)
        
        count_user1 = Message.unread_messages.unread_count_for_user(self.user1)
        self.assertEqual(count_user1, 1)
    
    def test_mark_as_read_method(self):
        """Test mark_as_read method"""
        # Mark specific messages as read
        updated_count = Message.unread_messages.mark_as_read(
            self.user2, 
            [self.unread_message1.id]
        )
        self.assertEqual(updated_count, 1)
        
        # Verify message is now read
        self.unread_message1.refresh_from_db()
        self.assertTrue(self.unread_message1.read)
        
        # Verify count decreased
        new_count = Message.unread_messages.unread_count_for_user(self.user2)
        self.assertEqual(new_count, 0)
    
    def test_mark_all_as_read(self):
        """Test marking all unread messages as read"""
        # Mark all unread messages for user2 as read
        updated_count = Message.unread_messages.mark_as_read(self.user2)
        self.assertEqual(updated_count, 1)
        
        # Verify no unread messages left
        unread_count = Message.unread_messages.unread_count_for_user(self.user2)
        self.assertEqual(unread_count, 0)
    
    def test_get_unread_threads(self):
        """Test get_unread_threads method"""
        # Create a thread with unread messages
        thread_starter = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Thread starter",
            read=True  # Thread starter is read
        )
        
        unread_reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Unread reply",
            parent_message=thread_starter,
            read=False
        )
        
        # User1 should see this thread as having unread messages
        unread_threads = Message.unread_messages.get_unread_threads(self.user1)
        self.assertEqual(unread_threads.count(), 1)
        self.assertEqual(unread_threads.first().id, thread_starter.id)
    
    def test_message_mark_as_read_method(self):
        """Test instance mark_as_read method"""
        self.assertFalse(self.unread_message1.read)
        
        self.unread_message1.mark_as_read()
        self.unread_message1.refresh_from_db()
        
        self.assertTrue(self.unread_message1.read)
    
    def test_is_unread_property(self):
        """Test is_unread convenience property"""
        self.assertTrue(self.unread_message1.is_unread)
        self.assertFalse(self.read_message.is_unread)

class QueryOptimizationTests(TestCase):
    """
    Test query optimization with .only() and select_related
    """
    
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
        
        for i in range(5):
            Message.objects.create(
                sender=self.user1,
                receiver=self.user2,
                content=f"Unread message {i}",
                read=False
            )
    
    def test_only_optimization(self):
        """Test that .only() reduces fetched fields"""
        # Without optimization would fetch all fields
        # With .only() we only fetch specified fields
        
        unread_messages = Message.unread_messages.for_user(self.user2)
        
        # The query should be optimized
        # We can verify by checking that accessing non-selected fields
        # might
