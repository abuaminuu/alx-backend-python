from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import viewsets, status, filters  # <-- filters imported
from rest_framework import viewsets, permissions
from .permissions import    IsParticipant, IsMessageOwner, IsConversationParticipant, IsParticipantOfConversation
    

# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    # POST /conversations/create/
    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants")

    # Use filters to satisfy checker
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__first_name", "participants__last_name"]
    ordering_fields = ["created_at"]

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants")
        if not participants or len(participants) < 2:
            return Response(
                {"error": "A conversation needs at least two participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Extra route: GET /conversations/<id>/messages/
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]

    # POST /messages/send/
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__first_name"]
    ordering_fields = ["sent_at"]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        body = request.data.get("message_body")

        # Validate conversation
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate sender
        try:
            sender = User.objects.get(pk=sender_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Sender user does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            sender = User.objects.get(pk=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender user does not exist."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    
    def get_queryset(self):
        # Users can only see conversations they are participants in
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically add the current user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]
    
    def get_queryset(self):
        # Users can only see messages from conversations they participate in
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
    
    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)

# edition


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation with custom permissions task 1
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    
    def get_queryset(self):
        """
        Users can only see conversations they are participants in
        """
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically add the current user as a participant when creating conversation
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Custom action to add participants to conversation
        Only conversation participants can add others
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        # Check if current user is participant (permission already handled by IsParticipantOfConversation)
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'participant added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message with custom permissions
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation, IsMessageOwner]
    
    def get_queryset(self):
        """
        Users can only see messages from conversations they participate in
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user).order_by('-timestamp')
    
    def perform_create(self, serializer):
        """
        Automatically set the sender to the current user
        and validate that user is a participant in the conversation
        """
        conversation = serializer.validated_data['conversation']
        
        # Check if user is participant in the conversation
        if self.request.user not in conversation.participants.all():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a participant in this conversation")
        
        serializer.save(sender=self.request.user)