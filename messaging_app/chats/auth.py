from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class to handle user authentication with JWT tokens.
    """
    def authenticate(self, request):
        try:
            # Get the header and validate it
            header = self.get_header(request)
            if header is None:
                return None

            # Get the raw token
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            # Validate the token and get the user
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            return (user, validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

class CustomSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication for browser-based API access.
    """
    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """
        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, no session user
        if not user or not user.is_authenticated:
            return None

        return (user, None)