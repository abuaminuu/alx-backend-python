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
