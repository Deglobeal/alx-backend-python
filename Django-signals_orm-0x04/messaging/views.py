from django.shortcuts import get_object_or_404, render
from .models import Message

def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all().order_by('-edited_at')
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'history': history
    })