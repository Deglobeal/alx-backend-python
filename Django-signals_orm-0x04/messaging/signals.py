from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created and not instance.parent_message:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Explicitly delete user-related messages, notifications, and histories"""
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()


@receiver(post_delete, sender=User)
def delete_user_related(sender, instance, **kwargs):
    # Delete all related data using cascade (handled by DB)
    # No explicit delete needed due to on_delete=CASCADE
    pass