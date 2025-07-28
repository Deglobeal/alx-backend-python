from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from django_filters import rest_framework as filters

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.none()

    def get_queryset(self) -> QuerySet:
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        conversation.participants.add(user)
        return Response({"status": "User added to conversation"}, status=status.HTTP_200_OK)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages in conversations.
    Only participants can view, send, update, or delete messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter
    queryset = Message.objects.all()

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        conversation_id = self.kwargs.get('conversation_pk')
        
        if conversation_id:
            return Message.objects.filter(
                conversation__id=conversation_id,
                conversation__participants=user
            ).order_by('-sent_at')
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation, 
            id=self.kwargs['conversation_pk']
        )
        serializer.save(
            sender=self.request.user, 
            conversation=conversation
        )

def root_view(request):
    return HttpResponse("""
    <h1>Messaging App API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/token/">JWT Token Obtain</a></li>
        <li><a href="/api/token/refresh/">JWT Token Refresh</a></li>
        <li><a href="/api/">API Root</a></li>
        <li><a href="/admin/">Admin Panel</a></li>
    </ul>
    """)