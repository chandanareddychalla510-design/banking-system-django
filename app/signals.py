from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Account
import random

@receiver(post_save, sender=User)
def create_user_profile_and_account(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        acc_num = "".join([str(random.randint(0, 9)) for _ in range(12)])
        Account.objects.create(user=instance, account_number=acc_num, balance=0.00)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    