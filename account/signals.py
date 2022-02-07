from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save,sender=settings.AUTH_USER_MODEL,)
def save_the_group(instance, raw, **kwargs):
    if not raw:
        to_add = Group.objects.get(name="group1")  # get_or_create is a better option
        instance.groups.add(to_add)
        instance.is_verified = True
        print("Working Fine")
        