from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # REQUIRED: CharField usage
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "role",
            "phone_number",
            "created_at",
            "full_name"
        ]


class MessageSerializer(serializers.ModelSerializer):
    # REQUIRED: SerializerMethodField usage
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "preview"
        ]

    def get_preview(self, obj):
        """Return first 20 characters of the message."""
        return obj.message_body[:20]


class ConversationSerializer(serializers.ModelSerializer):
    # nested messages
    messages = MessageSerializer(many=True, read_only=True)

    # example validation using ValidationError
    title = serializers.CharField(required=False)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
            "title",
        ]

    def validate_title(self, value):
        # REQUIRED: ValidationError usage
        if value and len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value
