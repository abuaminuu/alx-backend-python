from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # REQUIRED: CharField usage
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    sender = serializers.StringRelatedField(read_only=True)
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
        read_only_fields = ["sender", "timestamps"]

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
    participants = serializers.StringRelatedField(many=True, read_only=True)
   
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


# editions: Updated Serializers for Better Validation

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp', 'read']
        read_only_fields = ['sender', 'timestamp']
    
    def validate_conversation(self, value):
        """
        Validate that the current user is a participant in the conversation
        """
        user = self.context['request'].user
        if user not in value.participants.all():
            raise serializers.ValidationError("You are not a participant in this conversation")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

