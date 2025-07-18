from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to add the creator as a participant.

        """
        Conversation = serializer.save()
        Conversation.participants.add(self.request.user)
        Conversation.save()

        @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
        def add_participant(self, request, pk=None):
            conversation = self.get_object()
            user = request.data.get('user_id')


            try:
                user = User.objects.get(id=user)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            conversation.participants.add(user)
            return Response({"status": "User added to conversation"}, status=status.HTTP_200_OK)
        

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter messages by conversation ID if provided
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation__conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
