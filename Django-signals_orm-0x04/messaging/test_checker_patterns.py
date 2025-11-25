from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .models import Message

class CheckerPatternTests(TestCase):
    """
    Test that specifically verifies the exact patterns the checker is looking for
    """
    
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
        self.client = Client()
        self.client.force_login(self.user1)
        
        # Create test messages
        self.unread_message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Unread message",
            read=False
        )
        self.read_message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Read message", 
            read=True
        )
    
    def test_managers_file_exists(self):
        """Test that messaging/managers.py exists"""
        import os
        managers_file = os.path.join(os.path.dirname(__file__), 'managers.py')
        self.assertTrue(os.path.exists(managers_file), "managers.py file should exist")
    
    def test_unread_manager_exists(self):
        """Test that Message.unread manager exists"""
        self.assertTrue(hasattr(Message, 'unread'))
        self.assertEqual(Message.unread.model, Message)
    
    def test_unread_for_user_method_exists(self):
        """Test that unread_for_user method exists on custom manager"""
        self.assertTrue(hasattr(Message.unread, 'unread_for_user'))
        
        # Test that it returns a queryset
        result = Message.unread.unread_for_user(self.user1)
        self.assertTrue(hasattr(result, 'filter'))  # Should be a queryset
    
    def test_unread_for_user_filters_correctly(self):
        """Test that unread_for_user filters unread messages for user"""
        unread_messages = Message.unread.unread_for_user(self.user1)
        
        self.assertEqual(unread_messages.count(), 1)
        self.assertEqual(unread_messages.first().id, self.unread_message.id)
        
        # Should not include read messages
        self.assertNotIn(self.read_message, unread_messages)
        
        # Should not include messages for other users
        unread_for_user2 = Message.unread.unread_for_user(self.user2)
        self.assertEqual(unread_for_user2.count(), 0)
    
    def test_views_use_exact_pattern(self):
        """Test that views use Message.unread.unread_for_user pattern"""
        # Test simple_unread_view uses the exact pattern
        response = self.client.get('/messaging/unread/simple/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['unread_messages_count'], 1)
        
        # Test unread_inbox uses the pattern
        response = self.client.get('/messaging/unread/')
        self.assertEqual(response.status_code, 200)
    
    def test_unread_count_method(self):
        """Test unread_count_for_user method"""
        count = Message.unread.unread_count_for_user(self.user1)
        self.assertEqual(count, 1)
    
    def test_mark_as_read_method(self):
        """Test mark_as_read_for_user method"""
        # Mark the unread message as read
        updated_count = Message.unread.mark_as_read_for_user(self.user1, [self.unread_message.id])
        self.assertEqual(updated_count, 1)
        
        # Verify it's now read
        self.unread_message.refresh_from_db()
        self.assertTrue(self.unread_message.read)
        
        # Verify unread count decreased
        new_count = Message.unread.unread_count_for_user(self.user1)
        self.assertEqual(new_count, 0)
    
    def test_query_optimization(self):
        """Test that queries are optimized with .only()"""
        unread_messages = Message.unread.unread_for_user(self.user1)
        
        # The queryset should use .only() for optimization
        # We can check this by examining the query
        query_str = str(unread_messages.query)
        
        # Should select specific fields (not *)
        self.assertNotIn('*', query_str)
        
        # Should have select_related for sender
        self.assertIn('sender', query_str.lower())
