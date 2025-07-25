from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        # Allow only authenticated users
        if not request.user.is_authenticated:
            return False
        
        # For non-conversation actions, only require authentication
        if view.basename != 'conversation-messages':
            return True
            
        # For messages, check conversation participation
        conversation_id = view.kwargs.get('conversation_pk')
        if not conversation_id:
            return False
            
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
            return conversation.participants.filter(id=request.user.id).exists()
        except Conversation.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Allow only conversation participants to interact with messages
        return obj.conversation.participants.filter(id=request.user.id).exists()