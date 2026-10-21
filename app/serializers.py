from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Account, Transaction

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_image']

class RegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Account
        fields = ['account_number', 'balance', 'username']

class TransactionSerializer(serializers.ModelSerializer):
    from_account_number = serializers.CharField(source='from_account.account_number', read_only=True, default=None)
    to_account_number = serializers.CharField(source='to_account.account_number', read_only=True, default=None)

    class Meta:
        model = Transaction
        fields = ['id', 'from_account_number', 'to_account_number', 'amount', 'transaction_type', 'timestamp']