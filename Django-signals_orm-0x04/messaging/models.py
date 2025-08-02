from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from .managers import UnreadMessagesManager

User = get_user_model()

class MessageManager(models.Manager):
    def unread_for_user(self, user):
        """Custom manager method for unread messages"""
        return self.filter(receiver=user, read=False)
    
    def conversation_thread(self, user1, user2):
        """Get conversation thread between two users"""
        return self.filter(
            (Q(sender=user1) & Q(receiver=user2)) | 
            (Q(sender=user2) & Q(receiver=user1))
        ).order_by('timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # For unread tracking
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()   # Custom manager for unread messages

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:20]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_messages')

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"Edit at {self.edited_at} for Message #{self.message.pk}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about message #{self.message.pk}"
    
