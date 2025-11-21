from datetime import datetime

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