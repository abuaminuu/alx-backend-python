from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Message, Notification
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