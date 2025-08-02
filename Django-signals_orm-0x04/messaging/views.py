from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from .models import Message, Notification

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
    messages = Message.objects.conversation_between(
        request.user, other_user
    ).filter(parent_message__isnull=True)  # Only top-level messages
    
    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages
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

@login_required
def create_reply(request, parent_id):
    """Create a reply to a message"""
    parent_message = get_object_or_404(Message, id=parent_id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=parent_message.sender if request.user == parent_message.receiver else parent_message.receiver,
                content=content,
                parent_message=parent_message
            )
    return redirect('conversation_thread', user_id=parent_message.sender.pk)