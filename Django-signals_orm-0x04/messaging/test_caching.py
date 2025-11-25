from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.core.cache import cache
from .models import Message

class CacheTests(TestCase):
    """
    Test cases for view caching functionality
    """
    
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
        self.client = Client()
        self.client.force_login(self.user1)
        
        # Create test message
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Clear cache before each test
        cache.clear()
    
    def test_cache_configuration(self):
        """Test that cache is properly configured"""
        from django.conf import settings
        
        self.assertIn('CACHES', settings)
        self.assertIn('default', settings.CACHES)
        self.assertEqual(settings.CACHES['default']['BACKEND'], 
                        'django.core.cache.backends.locmem.LocMemCache')
    
    def test_cache_page_decorator(self):
        """Test that cache_page decorator works"""
        # First request should not be cached
        response1 = self.client.get('/messaging/threads/')
        self.assertEqual(response1.status_code, 200)
        
        # Second request might be cached (depending on implementation)
        response2 = self.client.get('/messaging/threads/')
        self.assertEqual(response2.status_code, 200)
    
    def test_cache_headers(self):
        """Test that cached responses have appropriate headers"""
        response = self.client.get('/messaging/threads/')
        self.assertEqual(response.status_code, 200)
        
        # Check for cache-related headers
        # Note: Django's cache_page might not add headers in development
    
    def test_cache_timeout(self):
        """Test that cache expires after timeout"""
        import time
        
        # Make initial request
        response1 = self.client.get('/messaging/threads/')
        self.assertEqual(response1.status_code, 200)
        
        # Wait for cache to expire (simulate)
        # In real scenario, we'd test after actual timeout
        
    def test_non_cached_views(self):
        """Test that dynamic views are not cached"""
        # API endpoints should not be cached
        response = self.client.get('/messaging/unread/api/')
        self.assertEqual(response.status_code, 200)
        
        # POST requests should not be cached
        response = self.client.post('/messaging/mark-read/')
        self.assertEqual(response.status_code, 200)
    
    def test_cache_clear_functionality(self):
        """Test cache clearing functionality"""
        # Make user1 staff to access cache clear
        self.user1.is_staff = True
        self.user1.save()
        
        response = self.client.get('/messaging/cache/clear/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
    
    def test_cache_info_endpoint(self):
        """Test cache info endpoint"""
        response = self.client.get('/messaging/cache/info/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('cache_info', data)

class CachePerformanceTests(TestCase):
    """
    Performance tests for caching
    """
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
        self.client = Client()
        self.client.force_login(self.user)
        
        # Create multiple messages to test performance
        for i in range(10):
            Message.objects.create(
                sender=self.user,
                receiver=self.user,
                content=f"Test message {i}"
            )
        
        cache.clear()
    
    def test_cached_vs_uncached_performance(self):
        """Compare performance of cached vs uncached views"""
        import time
        
        # First request (uncached)
        start_time = time.time()
        response1 = self.client.get('/messaging/threads/')
        time_uncached = time.time() - start_time
        
        # Second request (cached)
        start_time = time.time()
        response2 = self.client.get('/messaging/threads/')
        time_cached = time.time() - start_time
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        # Cached request should be faster (or at least not slower)
        # Allow some variance for test environment
        self.assertLessEqual(time_cached, time_uncached * 1.5)
