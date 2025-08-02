from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Renamed to timestamp
    edited = models.BooleanField(default=False)  # Track edit status

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:20]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()  # Previous content
    edited_at = models.DateTimeField(auto_now_add=True)  # Edit timestamp

    def __str__(self):
        return f"Edit at {self.edited_at} for Message #{self.message.id}"