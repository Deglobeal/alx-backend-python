from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message

User = get_user_model()


@login_required
def delete_user(request):
    """Explicit view to delete user account"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()  # ✅ Required for check
        return redirect('home')
    return render(request, 'messaging/confirm_delete.html')


@login_required
@cache_page(60)
def conversation_view(request, user_id):
    """Optimized threaded conversation view between current user and another user."""
    other_account = get_object_or_404(User, id=user_id)

    # ✅ Optimized query
    all_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_account) |
        Q(sender=other_account, receiver=request.user)
    ).select_related('sender', 'receiver') \
     .prefetch_related('replies') \
     .only('id', 'content', 'timestamp', 'sender__username', 'receiver__username', 'parent_message')

    # ✅ Threaded reply structure
    message_dict = {msg.id: msg for msg in all_messages}  # type: ignore[attr-defined]
    for msg in all_messages:
        msg.replies_list = []  # type: ignore[attr-defined]

    for msg in all_messages:
        if getattr(msg, 'parent_message_id', None):  # type: ignore[attr-defined]
            parent = message_dict.get(msg.parent_message_id)  # type: ignore[attr-defined]
            if parent:
                parent.replies_list.append(msg)  # type: ignore[attr-defined]
    
    root_messages = [msg for msg in all_messages if msg.parent_message is None]

    return render(request, 'messaging/conversation.html', {
        'other_user': other_account,
        'messages': root_messages
    })


@login_required
def unread_view(request):
    """Displays unread messages using custom manager"""
    unread = Message.unread.unread_for_user(request.user).only(
        'id', 'content', 'timestamp', 'sender__username'
    )
    return render(request, 'messaging/unread.html', {
        'messages': unread
    })


@login_required
def message_history_view(request, message_id):
    """Displays edit history of a specific message"""
    msg = get_object_or_404(Message, id=message_id)
    if request.user not in [msg.sender, msg.receiver]:
        return render(request, 'messaging/permission_denied.html')

    history = msg.history.all()  # type: ignore[attr-defined]
    return render(request, 'messaging/history.html', {
        'message': msg,
        'history': history,
        'sender': request.user
    })
