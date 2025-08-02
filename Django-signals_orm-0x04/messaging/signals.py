from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification, User

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
    if created and not instance.parent_message:  # Only for new top-level messages
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def delete_user_related(sender, instance, **kwargs):
    # CASCADE deletes handle related data automatically
    # No explicit deletion needed due to on_delete=CASCADE
    pass