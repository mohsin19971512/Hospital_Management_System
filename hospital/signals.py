from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import OutPatients
User = get_user_model()

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # print('sender', sender)
    print('instance', instance.phone_number)
    if created and instance.type == "patient":
        OutPatients.objects.create(user=instance,phone_number=instance.phone_number,first_name=instance.first_name,last_name=instance.last_name)











"""@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # print('sender', sender)
    # print('instance', instance)
    if created:
        Patient_Info_in_Hospital.objects.create(user=instance)"""