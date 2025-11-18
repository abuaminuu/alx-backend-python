from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow conversation participants to access messages.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    - Allows any authenticated user to access the API
    - Allows only conversation participants to perform actions on messages
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated for any API access
        """
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation for object-level access
        """
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # For Message objects
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        # For other objects, default to safe methods only
        return request.method in permissions.SAFE_METHODS


class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow message owners to update or delete their messages
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any participant
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the message sender
        return obj.sender == request.user


class IsConversationOwner(permissions.BasePermission):
    """
    Custom permission to allow conversation creators additional privileges
    """
    def has_object_permission(self, request, view, obj):
        # For creation, we might want to check if user can add participants
        if request.method == 'POST':
            return True
        
        # For other operations, allow if user is participant
        return request.user in obj.participants.all()


# Update Permissions with Explicit Method Handling (PUT PATCH DELETE)
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    - Allow only authenticated users to access the API
    - Allow only participants in a conversation to send, view, update and delete messages
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated for any API access
        """
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation for object-level access
        Specifically handle PUT, PATCH, DELETE methods
        """
        # Check if user is participant for conversation objects
        if hasattr(obj, 'participants'):
            is_participant = request.user in obj.participants.all()
            
            # For PUT, PATCH, DELETE - require participant status
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return is_participant
            
            # For GET, POST, etc. - allow if participant
            return is_participant
        
        # Check if user is participant for message objects
        elif hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
            
            # For PUT, PATCH, DELETE - require participant status
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return is_participant
            
            # For GET, POST, etc. - allow if participant
            return is_participant
        
        # Default deny for other objects
        return False


class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow message owners to update or delete their messages
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS) are allowed for any participant
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions (PUT, PATCH, DELETE) are only allowed to the message sender
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender == request.user
        
        # For POST, check if user is participant in conversation
        return request.user in obj.conversation.participants.all()


class IsConversationOwner(permissions.BasePermission):
    """
    Custom permission to allow conversation creators additional privileges
    """
    def has_object_permission(self, request, view, obj):
        # For POST - allow if user is authenticated
        if request.method == 'POST':
            return True
        
        # For PUT, PATCH, DELETE - require participant status
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()
        
        # For GET - allow if participant
        return request.user in obj.participants.all()

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Explicitly handles PUT, PATCH, DELETE methods as required.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated for any API access
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions with explicit method handling
        """
        # Handle PUT method
        if request.method == 'PUT':
            return self._check_participant_access(request.user, obj)
        
        # Handle PATCH method  
        elif request.method == 'PATCH':
            return self._check_participant_access(request.user, obj)
        
        # Handle DELETE method
        elif request.method == 'DELETE':
            return self._check_participant_access(request.user, obj)
        
        # Handle other methods (GET, POST, etc.)
        else:
            return self._check_participant_access(request.user, obj)
    
    def _check_participant_access(self, user, obj):
        """
        Helper method to check if user is participant in conversation
        """
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False
