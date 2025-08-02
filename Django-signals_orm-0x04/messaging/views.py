from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
from .models import Message, User

@login_required
def delete_user(request):
    """View to delete user account"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')  # Redirect to home after deletion
    return render(request, 'messaging/confirm_delete.html')

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_thread(request, user_id):
    """View conversation thread between current user and another user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Get all messages in the conversation
    messages = Message.objects.conversation_thread(
        request.user, other_user
    ).select_related('sender', 'receiver')
    
    # Build threaded structure
    messages_dict = {}
    for message in messages:
        message.replies = []
        messages_dict[message.id] = message
    
    root_messages = []
    for message in messages:
        if message.parent_message_id:
            parent = messages_dict.get(message.parent_message_id)
            if parent:
                parent.replies.append(message)
        else:
            root_messages.append(message)
    
    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': root_messages
    })

@login_required
def unread_messages(request):
    """View for unread messages using custom manager"""
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'content', 'sender__username', 'timestamp'
    )
    return render(request, 'messaging/unread.html', {
        'unread_messages': unread_messages
    })

@login_required
def message_history(request, message_id):
    """View message edit history"""
    message = get_object_or_404(Message, id=message_id)
    if request.user not in [message.sender, message.receiver]:
        return render(request, 'messaging/permission_denied.html')
    history = message.history.all()
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })