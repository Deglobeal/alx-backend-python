from django.shortcuts import get_object_or_404, render
from .models import Message, Notification

def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all().order_by('-history_date') if hasattr(message, 'history') else []
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