import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth.models import User
from messaging.models import Message, Notification

# Create test users
sender, created = User.objects.get_or_create(username='test_sender')
receiver, created = User.objects.get_or_create(username='test_receiver')

print("Testing message signals...")

# Create a message (this should trigger the signal)
message = Message.objects.create(
    sender=sender,
    receiver=receiver,
    content="This is a test message to trigger notifications!"
)

print(f"Message created: {message}")
print(f"Notifications created: {Notification.objects.count()}")

# Check the notification
notification = Notification.objects.first()
if notification:
    print(f"Notification details: {notification}")
    print(f"Notification title: {notification.title}")
    print(f"Notification preview: {notification.message_preview}")