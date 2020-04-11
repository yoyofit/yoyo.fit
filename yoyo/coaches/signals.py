import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Coach


@receiver(post_delete, sender=Coach)
def submission_delete(sender: Coach, instance: Coach, **kwargs):
    if instance.hero_photo:
        if os.path.isfile(instance.hero_photo.path):
            os.remove(instance.hero_photo.path)


@receiver(pre_save, sender=Coach)
def submission_update(sender: Coach, instance: Coach, **kwargs):
    if not instance.pk:
        return False

    try:
        old_hero_photo = sender.objects.get(pk=instance.pk).hero_photo
    except sender.DoesNotExist:
        return False

    if instance.hero_photo and old_hero_photo:
        new_hero_photo = instance.hero_photo
        if not old_hero_photo == new_hero_photo:
            if os.path.isfile(old_hero_photo.path):
                os.remove(old_hero_photo.path)
