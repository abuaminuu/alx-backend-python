from django.db import models
from django.db.models import Q

class UnreadMessagesManager(models.Manager):
    """
    Custom manager for filtering unread messages with optimizations
    """
    
    def unread_for_user(self, user):
        """
        Filter unread messages for a specific user with optimization
        Uses .only() to retrieve only necessary fields
        """
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related(
            'sender'
        ).only(
            'id', 'content', 'timestamp', 'sender__username', 'sender__id',
            'thread_depth', 'parent_message_id', 'read'
        ).order_by('-timestamp')
    
    def unread_count_for_user(self, user):
        """
        Get count of unread messages for a user (optimized for counting)
        """
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).count()
    
    def mark_as_read_for_user(self, user, message_ids=None):
        """
        Mark messages as read for a user
        If message_ids is provided, only mark those specific messages
        """
        queryset = self.get_queryset().filter(receiver=user, read=False)
        
        if message_ids:
            queryset = queryset.filter(id__in=message_ids)
        
        return queryset.update(read=True)

class MessageManager(models.Manager):
    """
    Default manager for Message model with additional methods
    """
    
    def get_threads_for_user(self, user):
        """
        Get all thread starters for a user
        """
        return self.get_queryset().filter(
            Q(sender=user) | Q(receiver=user),
            is_thread_starter=True
        ).select_related('sender', 'receiver').order_by('-timestamp')
    
    def get_complete_thread(self, thread_starter_id):
        """
        Get entire thread with all replies
        """
        return self.get_queryset().filter(
            Q(id=thread_starter_id) |
            Q(parent_message_id=thread_starter_id) |
            Q(parent_message__parent_message_id=thread_starter_id)
        ).select_related('sender', 'receiver').order_by('thread_depth', 'timestamp')

        