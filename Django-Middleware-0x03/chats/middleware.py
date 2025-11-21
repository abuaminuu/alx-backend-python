from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    """
    Middleware to log each user's requests including timestamp, user, and request path
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Create log message
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method}\n"
        
        # Write to file
        with open('user_requests.log', 'a') as log_file:
            log_file.write(log_message)
        
        # Process the request and get response
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to messaging app between 9 PM (21:00) and 6 AM (06:00)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get current time
        current_time = datetime.now().time()
        
        # Define restricted hours: 9 PM (21:00) to 6 AM (06:00)
        restricted_start = time(21, 0)  # 9:00 PM
        restricted_end = time(6, 0)     # 6:00 AM
        
        # Check if current time is within restricted hours
        is_restricted = self.is_time_restricted(current_time, restricted_start, restricted_end)
        
        # Check if the request is for messaging endpoints
        if self.is_messaging_endpoint(request.path) and is_restricted:
            return HttpResponseForbidden(
                "Access to messaging services is restricted between 9 PM and 6 AM. "
                "Please try again during allowed hours."
            )
        
        # Process the request normally if not restricted
        response = self.get_response(request)
        return response
    
    def is_time_restricted(self, current_time, start_time, end_time):
        """
        Check if current time falls within restricted hours (9 PM to 6 AM)
        """
        if start_time < end_time:
            # Normal case: restriction within same day
            return start_time <= current_time <= end_time
        else:
            # Overnight case: restriction spans midnight
            return current_time >= start_time or current_time <= end_time
    
    def is_messaging_endpoint(self, path):
        """
        Check if the request path is for messaging-related endpoints
        """
        messaging_paths = [
            '/api/conversations/',
            '/api/messages/',
            '/api/chats/',
            '/api/chat/'
        ]
        
        # Check if path starts with any messaging endpoint
        return any(path.startswith(messaging_path) for messaging_path in messaging_paths)



class RateLimitMiddleware:
    """
    Middleware that limits the number of messages a user can send based on IP address
    Limit: 5 messages per minute per IP
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts per IP: {ip: [timestamp1, timestamp2, ...]}
        self.request_log = {}
        self.limit = 5  # 5 messages
        self.window = 60  # 1 minute in seconds
    
    def __call__(self, request):
        # Only check POST requests to messaging endpoints
        if request.method == 'POST' and self.is_messaging_endpoint(request.path):
            # Get client IP address
            ip = self.get_client_ip(request)
            
            # Check rate limit
            if self.is_rate_limited(ip):
                return HttpResponseForbidden(
                    f"Rate limit exceeded. Maximum {self.limit} messages per {self.window} seconds. "
                    f"Please wait before sending more messages."
                )
            
            # Record this request
            self.record_request(ip)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
    
    def is_messaging_endpoint(self, path):
        """
        Check if the request path is for messaging endpoints
        """
        messaging_paths = ['/api/messages/', '/api/chats/']
        return any(path.startswith(messaging_path) for messaging_path in messaging_paths)
    
    def is_rate_limited(self, ip):
        """
        Check if the IP has exceeded the rate limit
        """
        current_time = time.time()
        
        # Initialize if IP not in log
        if ip not in self.request_log:
            self.request_log[ip] = []
        
        # Remove old timestamps (outside the time window)
        window_start = current_time - self.window
        self.request_log[ip] = [timestamp for timestamp in self.request_log[ip] if timestamp > window_start]
        
        # Check if limit exceeded
        return len(self.request_log[ip]) >= self.limit
    
    def record_request(self, ip):
        """
        Record a request timestamp for the IP
        """
        current_time = time.time()
        self.request_log[ip].append(current_time)
        
        # Clean up old IPs to prevent memory leaks (optional)
        self.cleanup_old_entries()
    
    def cleanup_old_entries(self):
        """
        Remove IP entries that haven't been used in the last hour
        """
        current_time = time.time()
        one_hour_ago = current_time - 3600
        
        ips_to_remove = []
        for ip, timestamps in self.request_log.items():
            # If no recent activity, mark for removal
            if not timestamps or max(timestamps) < one_hour_ago:
                ips_to_remove.append(ip)
        
        for ip in ips_to_remove:
            del self.request_log[ip]