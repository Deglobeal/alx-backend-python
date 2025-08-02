from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Existing message being updated
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # Content changed
                # Create history record before update
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True  # Mark as edited
        except Message.DoesNotExist:
            pass  # New message, skip history

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:  # Only for new messages
        # Create notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )