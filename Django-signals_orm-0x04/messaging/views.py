from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Notification

def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Remove history attribute access since it does not exist
    history = []
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'history': history
    })

def user_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return render(request, 'messaging/notifications.html', {
        'notifications': notifications
    })

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Verify user has permission (sender or receiver)
    if request.user not in [message.sender, message.receiver]:
        return render(request, 'messaging/permission_denied.html')
    
    # Since 'history' attribute does not exist, just pass the message itself or implement history logic if needed
    history = []  # Placeholder for message history if implemented later
    
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

@login_required
def message_list(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | 
        Q(receiver=request.user)
    ).order_by('-timestamp')
    
    return render(request, 'messaging/message_list.html', {
        'messages': messages
    })