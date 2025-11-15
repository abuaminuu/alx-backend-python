from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(auto_now_add=True)

    # Enforce unique email
    email = models.EmailField(unique=True)

    # Remove username if you prefer email-login only:
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"  # change to "email" only if you disable username

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"


class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    participants = models.ManyToManyField(
        User,
        related_name="conversations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    message_body = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message from {self.sender.username}"
