from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models.query import QuerySet
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
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

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        conversation.participants.add(user)
        return Response({"status": "User added to conversation"}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    queryset = Message.objects.none()

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        queryset = Message.objects.filter(conversation__participants=user)

        conversation_id = self.request.GET.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if conversation and self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            raise PermissionDenied("You are not allowed to update this message.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            raise PermissionDenied("You are not allowed to delete this message.")
        return super().destroy(request, *args, **kwargs)


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
