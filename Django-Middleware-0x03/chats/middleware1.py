import logging
from datetime import datetime

# Configure logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler('user_requests.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)

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
        
        # Log the request information
        log_message = f"User: {user} - Path: {request.path} - Method: {request.method}"
        logger.info(log_message)
        
        # Process the request and get response
        response = self.get_response(request)
        
        return response