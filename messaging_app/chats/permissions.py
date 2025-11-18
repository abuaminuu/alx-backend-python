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
