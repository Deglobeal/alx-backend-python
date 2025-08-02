# messaging/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # Track edit status

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
    
# messaging/models.py
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()  # Previous content
    edited_at = models.DateTimeField(auto_now_add=True)  # Edit timestamp

    def __str__(self):
        return f"Edit at {self.edited_at} for Message #{self.message.id}"