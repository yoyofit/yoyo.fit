import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Institute


@receiver(post_delete, sender=Institute)
def submission_delete(sender: Institute, instance: Institute, **kwargs):
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


@receiver(pre_save, sender=Institute)
def submission_update(sender: Institute, instance: Institute, **kwargs):
    if not instance.pk:
        return False

    try:
        old_logo = sender.objects.get(pk=instance.pk).logo
    except sender.DoesNotExist:
        return False

    new_logo = instance.logo
    if not old_logo == new_logo:
        if os.path.isfile(old_logo.path):
            os.remove(old_logo.path)
