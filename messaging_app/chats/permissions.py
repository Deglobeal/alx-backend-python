from rest_framework.permissions import BasePermission
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Handles all HTTP methods (GET, POST, PUT, PATCH, DELETE)
    """
    def has_permission(self, request, view):
        # Allow only authenticated users
        if not request.user.is_authenticated:
            return False
            
        # For messages, check conversation participation
        if view.basename == 'conversation-messages':
            conversation_id = view.kwargs.get('conversation_pk')
            if not conversation_id:
                return False
                
            try:
                conversation = Conversation.objects.get(pk=conversation_id)
                return conversation.participants.filter(id=request.user.id).exists()
            except Conversation.DoesNotExist:
                return False
                
        # For other endpoints, only require authentication
        return True

    def has_object_permission(self, request, view, obj):
        # For messages, check if user is participant in the conversation
        if view.basename == 'conversation-messages':
            return obj.conversation.participants.filter(id=request.user.id).exists()
            
        # For conversations, check if user is participant
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
            
        return True

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        # Write permissions are only allowed to the owner of the object.
        return obj == request.user