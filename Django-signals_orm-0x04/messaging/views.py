from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

@login_required
def account_delete(request):
    if request.method == 'POST':
        account = request.user
        logout(request)
        account.delete()
        return redirect('home')
    return render(request, 'messaging/confirm_delete.html')

@login_required
@cache_page(60)
def conversation_view(request, user_id):
    other_account = get_object_or_404(User, id=user_id)

    # Get messages in conversation
    messages = Message.objects.conversation_between(
        request.user, other_account
    ).prefetch_related('replies')  # fixed from 'children' to 'replies'

    # Build threaded structure
    message_dict = {}
    root_messages = []

    for m in messages:
        m.replies_list = []  # temporary attribute to build thread
        message_dict[m.id] = m

    for m in messages:
        if m.parent_message_id:
            parent = message_dict.get(m.parent_message_id)
            if parent:
                parent.replies_list.append(m)
        else:
            root_messages.append(m)

    return render(request, 'messaging/conversation.html', {
        'other_user': other_account,
        'messages': root_messages
    })

@login_required
def unread_view(request):
    unread = Message.unread.unread_for_user(request.user).only(
        'id', 'content', 'timestamp', 'sender__username'
    )
    return render(request, 'messaging/unread.html', {
        'messages': unread
    })

@login_required
def message_history_view(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    if request.user not in [msg.sender, msg.receiver]:
        return render(request, 'messaging/permission_denied.html')

    history = msg.history.all()
    return render(request, 'messaging/history.html', {
        'message': msg,
        'history': history
    })
