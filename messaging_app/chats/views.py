from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import HttpResponse

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Conversation.objects.none()  # Initialize with empty queryset

    def get_queryset(self) -> QuerySet[Conversation]:
        # Return only conversations that include the current user
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.none()  # Initialize with empty queryset

    def get_queryset(self):
        # Return only messages from conversations the user participates in
        user = self.request.user
        queryset = Message.objects.filter(conversation__participants=user)
        
        # Optional filtering by conversation ID
        conversation_id = self.request.GET.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


    
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