from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create a notification when a new message is created
    """
    if created:
        try:
            # Create notification for the receiver
            notification = Notification.objects.create(
                user=instance.receiver,
                message=instance,
                notification_type='new_message',
                title=f"New message from {instance.sender.username}",
                message_preview=instance.content[:100] + "..." if len(instance.content) > 100 else instance.content
            )
            print(f"Notification created: {notification}")  # For debugging
        except Exception as e:
            print(f"Error creating notification: {e}")

@receiver(pre_save, sender=Message)
def update_message_read_status(sender, instance, **kwargs):
    """
    Signal to create a notification when a message is marked as read
    """
    if instance.pk:  # Only for existing instances (updates)
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if not old_instance.is_read and instance.is_read:
                # Message was just marked as read
                Notification.objects.create(
                    user=instance.sender,
                    message=instance,
                    notification_type='message_read',
                    title=f"{instance.receiver.username} read your message",
                    message_preview=f"Your message was read: {instance.content[:50]}..."
                )
        except Message.DoesNotExist:
            pass  # New instance, no old instance to compare

@receiver(post_save, sender=Message)
def send_real_time_notification(sender, instance, created, **kwargs):
    """
    Additional signal for potential real-time notifications (WebSocket integration)
    """
    if created:
        # This is where you would integrate with WebSockets, push notifications, etc.
        # For now, we'll just log it
        print(f"Real-time notification would be sent to {instance.receiver.username}")
        
        # Example: Integrate with WebSocket or push notification service
        # websocket_manager.send_notification(
        #     user_id=instance.receiver.id,
        #     notification_type='new_message',
        #     data={
        #         'sender': instance.sender.username,
        #         'message_preview': instance.content[:50],
        #         'message_id': instance.id
        #     }
        # )
