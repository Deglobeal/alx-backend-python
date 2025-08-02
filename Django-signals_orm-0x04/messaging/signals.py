# messaging/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only trigger for existing messages (updates)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content changed
            if old_message.content != instance.content:
                # Create history record
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass  # New instance, ignore