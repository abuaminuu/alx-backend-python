from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    """
    Enhanced middleware to log detailed request information
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get user information
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = f"{request.user.username} (ID: {request.user.id})"
        else:
            user = "Anonymous"
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
        
        # Create detailed log message
        log_message = (
            f"{datetime.now()} - "
            f"User: {user} - "
            f"IP: {ip} - "
            f"Path: {request.path} - "
            f"Method: {request.method} - "
            f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
        )
        
        # Log the message
        logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response
    