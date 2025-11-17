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

class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow message sender to access their messages.
    """
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow conversation participants to access messages.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()