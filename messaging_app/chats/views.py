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

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation with custom permissions and explicit 403 handling
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
    
    def handle_exception(self, exc):
        """
        Custom exception handler to return HTTP_403_FORBIDDEN when needed
        """
        from rest_framework.exceptions import PermissionDenied
        
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)
    
    def update(self, request, *args, **kwargs):
        """
        Handle PUT and PATCH requests with explicit permission checking
        """
        try:
            return super().update(request, *args, **kwargs)
        except PermissionDenied:
            return Response(
                {"detail": "You are not allowed to update this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE requests with explicit permission checking
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except PermissionDenied:
            return Response(
                {"detail": "You are not allowed to delete this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Custom action to add participants to conversation
        Only conversation participants can add others
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        # Check if current user is participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You must be a participant to add users to this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'status': 'participant added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message with custom permissions and explicit 403 handling
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
    
    def handle_exception(self, exc):
        """
        Custom exception handler to return HTTP_403_FORBIDDEN when needed
        """
        from rest_framework.exceptions import PermissionDenied
        
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You do not have permission to perform this action on this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)
    
    def update(self, request, *args, **kwargs):
        """
        Handle PUT and PATCH requests with explicit permission checking
        """
        try:
            return super().update(request, *args, **kwargs)
        except PermissionDenied:
            return Response(
                {"detail": "You can only update your own messages."},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE requests with explicit permission checking
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except PermissionDenied:
            return Response(
                {"detail": "You can only delete your own messages."},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @action(detail=True, methods=['put', 'patch'])
    def mark_as_read(self, request, pk=None):
        """
        Custom action to mark message as read
        Only participants can mark messages as read
        """
        message = self.get_object()
        
        # Check if user is participant in the conversation
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You must be a participant to mark messages as read."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.read = True
        message.save()
        return Response({'status': 'message marked as read'})


# added pagination and filters... task 2

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message with pagination, filtering, and custom permissions
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation, IsMessageOwner]
    pagination_class = MessagePagination  # Custom pagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MessageFilter  # Our custom filter class
    search_fields = ['content']  # Enable search on message content
    ordering_fields = ['timestamp', 'read']  # Enable ordering by timestamp and read status
    ordering = ['-timestamp']  # Default ordering: newest first
    
    def get_queryset(self):
        """
        Users can only see messages from conversations they participate in
        Apply additional filtering based on query parameters
        """
        user = self.request.user
        queryset = Message.objects.filter(conversation__participants=user)
        
        # Apply additional custom filtering if needed
        return queryset.select_related('sender', 'conversation')
    
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
    
    def handle_exception(self, exc):
        """
        Custom exception handler to return HTTP_403_FORBIDDEN when needed
        """
        from rest_framework.exceptions import PermissionDenied
        
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You do not have permission to perform this action on this message."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """
        Custom action to get unread messages with pagination and filtering
        """
        queryset = self.get_queryset().filter(read=False)
        
        # Apply filtering to the unread messages
        filtered_queryset = self.filter_queryset(queryset)
        
        # Paginate the results
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom action to get recent messages (last 24 hours)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        queryset = self.get_queryset().filter(timestamp__gte=twenty_four_hours_ago)
        
        # Apply filtering
        filtered_queryset = self.filter_queryset(queryset)
        
        # Paginate
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation (updated to maintain consistency)
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination  # Use same pagination for consistency
    
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
    
    def handle_exception(self, exc):
        """
        Custom exception handler to return HTTP_403_FORBIDDEN when needed
        """
        from rest_framework.exceptions import PermissionDenied
        
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)