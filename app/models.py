from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    address = models.TextField(
        blank=True,
        null=True
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.jpg'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account'
    )
    account_number = models.CharField(
        max_length=12,
        unique=True
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    )

    from_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions'
    )

    to_account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transactions'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
)
    

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"