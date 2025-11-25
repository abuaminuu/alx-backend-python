from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# with signal
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

# without signal
class Message(models.Model):
    """
    Message model for storing chat messages between users
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'timestamp']),
            models.Index(fields=['sender', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-edited_at']
    
    def __str__(self):
        return f"History for Message {self.message.id} - {self.edited_at}"


class Notification(models.Model):
    """
    Notification model to store user notifications for new messages
    """
    NOTIFICATION_TYPES = [
        ('new_message', 'New Message'),
        ('message_read', 'Message Read'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES, 
        default='new_message'
    )
    title = models.CharField(max_length=200)
    message_preview = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', 'created_at']),
        ]
    
    def __str__(self):
        return f"Notification for {self.user}: {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save()


class Message(models.Model):
    """
    Enhanced Message model with threaded conversation support
    """
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    # FIX: Add parent_message field (self-referential foreign key)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True,
        verbose_name='Parent Message'
    )
    
    # Additional fields for threading
    thread_depth = models.PositiveIntegerField(default=0)
    is_thread_starter = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['thread_depth', 'timestamp']
        indexes = [
            models.Index(fields=['receiver', 'timestamp']),
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['parent_message', 'timestamp']),
            models.Index(fields=['thread_depth', 'timestamp']),
        ]
    
    def __str__(self):
        if self.parent_message:
            return f"Reply from {self.sender} to {self.parent_message.sender}'s message"
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        """Override save to handle thread depth calculation"""
        if self.parent_message:
            self.thread_depth = self.parent_message.thread_depth + 1
            self.is_thread_starter = False
            self.receiver = self.parent_message.sender
        else:
            self.thread_depth = 0
            self.is_thread_starter = True
        
        super().save(*args, **kwargs)
    
    def get_thread_replies(self, include_self=True):
        """
        Get all replies in this thread using recursive-like query
        """
        if include_self:
            base_query = Message.objects.filter(
                Q(id=self.id) | 
                Q(parent_message=self) |
                Q(parent_message__parent_message=self) |
                Q(parent_message__parent_message__parent_message=self)
            )
        else:
            base_query = Message.objects.filter(
                Q(parent_message=self) |
                Q(parent_message__parent_message=self) |
                Q(parent_message__parent_message__parent_message=self)
            )
        
        return base_query.select_related('sender', 'receiver', 'parent_message')
    
    @property
    def reply_count(self):
        return self.replies.count()
    
    @property
    def direct_reply_count(self):
        return self.replies.filter(thread_depth=self.thread_depth + 1).count()

# Keep existing Notification and other models...

class UnreadMessagesManager(models.Manager):
    """
    Custom manager for filtering unread messages with optimizations
    """
    
    def for_user(self, user):
        """
        Get unread messages for a specific user with optimized queries
        Uses .only() to retrieve only necessary fields
        """
        return self.filter(
            receiver=user,
            is_read=False
        ).select_related(
            'sender'
        ).only(
            'id', 'content', 'timestamp', 'sender__username', 'sender__id',
            'thread_depth', 'parent_message_id'
        ).order_by('-timestamp')
    
    def unread_count_for_user(self, user):
        """
        Get count of unread messages for a user (optimized for counting)
        """
        return self.filter(
            receiver=user,
            is_read=False
        ).count()
    
    def mark_as_read(self, user, message_ids=None):
        """
        Mark messages as read for a user
        If message_ids is provided, only mark those specific messages
        """
        queryset = self.filter(receiver=user, is_read=False)
        
        if message_ids:
            queryset = queryset.filter(id__in=message_ids)
        
        return queryset.update(is_read=True)
    
    def get_unread_threads(self, user):
        """
        Get thread starters that have unread messages with optimization
        """
        # Get thread starters where user has unread messages
        return self.filter(
            Q(receiver=user, is_read=False) |
            Q(replies__receiver=user, replies__is_read=False)
        ).filter(
            is_thread_starter=True
        ).select_related(
            'sender', 'receiver'
        ).prefetch_related(
            'replies'
        ).only(
            'id', 'content', 'timestamp', 'sender__username', 
            'receiver__username', 'thread_depth'
        ).distinct().order_by('-timestamp')

class Message(models.Model):
    """
    Enhanced Message model with read status and custom managers
    """
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # FIX: Add read boolean field (renamed from is_read for clarity)
    read = models.BooleanField(default=False, verbose_name='Is Read')
    
    # Threading support
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True,
        verbose_name='Parent Message'
    )
    thread_depth = models.PositiveIntegerField(default=0)
    is_thread_starter = models.BooleanField(default=True)
    
    # Custom managers
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager for unread messages
    
    class Meta:
        ordering = ['thread_depth', 'timestamp']
        indexes = [
            models.Index(fields=['receiver', 'timestamp']),
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['parent_message', 'timestamp']),
            models.Index(fields=['thread_depth', 'timestamp']),
            models.Index(fields=['receiver', 'read', 'timestamp']),  # For unread queries
        ]
    
    def __str__(self):
        if self.parent_message:
            return f"Reply from {self.sender} to {self.parent_message.sender}'s message"
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        """Override save to handle thread depth calculation"""
        if self.parent_message:
            self.thread_depth = self.parent_message.thread_depth + 1
            self.is_thread_starter = False
            self.receiver = self.parent_message.sender
        else:
            self.thread_depth = 0
            self.is_thread_starter = True
        
        super().save(*args, **kwargs)
    
    def mark_as_read(self):
        """Mark this message as read"""
        self.read = True
        self.save(update_fields=['read'])
    
    @property
    def is_unread(self):
        """Convenience property to check if message is unread"""
        return not self.read
    
    def get_thread_replies(self, include_self=True):
        """
        Get all replies in this thread using recursive-like query
        """
        if include_self:
            base_query = Message.objects.filter(
                Q(id=self.id) | 
                Q(parent_message=self) |
                Q(parent_message__parent_message=self) |
                Q(parent_message__parent_message__parent_message=self)
            )
        else:
            base_query = Message.objects.filter(
                Q(parent_message=self) |
                Q(parent_message__parent_message=self) |
                Q(parent_message__parent_message__parent_message=self)
            )
        
        return base_query.select_related('sender', 'receiver', 'parent_message')
    
    @property
    def reply_count(self):
        return self.replies.count()
    
    @property
    def direct_reply_count(self):
        return self.replies.filter(thread_depth=self.thread_depth + 1).count()

# Update Notification model to use the new read field
class Notification(models.Model):
    """
    Notification model (updated to maintain consistency)
    """
    NOTIFICATION_TYPES = [
        ('new_message', 'New Message'),
        ('message_read', 'Message Read'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES, 
        default='new_message'
    )
    title = models.CharField(max_length=200)
    message_preview = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user}: {self.title}"

# Keep other models...