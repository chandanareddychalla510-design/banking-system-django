from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from decimal import Decimal
from django.db import transaction
from django.db.models import Q
from .models import Account, Transaction
from .serializers import (
    RegisterSerializer, UserSerializer, AccountSerializer, TransactionSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        profile = user.profile
        
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()

        profile.phone = request.data.get('phone', profile.phone)
        profile.address = request.data.get('address', profile.address)
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        profile.save()

        return Response(UserSerializer(user).data)

class AccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = Decimal(request.data.get('amount'))
            account = Account.objects.get(user=request.user)

            if amount <= 0:
                return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

            account.balance += amount
            account.save()

            Transaction.objects.create(
                to_account=account,
                amount=amount,
                transaction_type="deposit"
            )

            return Response({
                "message": "Deposit successful",
                "balance": account.balance
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = Decimal(request.data.get('amount'))
            account = Account.objects.get(user=request.user)

            if amount <= 0:
                return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

            if account.balance < amount:
                return Response({"error": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)

            account.balance -= amount
            account.save()

            Transaction.objects.create(
                from_account=account,
                amount=amount,
                transaction_type="withdraw"
            )

            return Response({
                "message": "Withdraw successful",
                "balance": account.balance
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = Decimal(request.data.get('amount'))
            to_account_num = request.data.get('to_account')
            
            sender_acc = Account.objects.get(user=request.user)
            receiver_acc = Account.objects.get(account_number=to_account_num)

            if amount <= 0 or sender_acc.balance < amount:
                return Response({"error": "Invalid amount or insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                sender_acc.balance -= amount
                receiver_acc.balance += amount
                sender_acc.save()
                receiver_acc.save()

                Transaction.objects.create(
                    from_account=sender_acc,
                    to_account=receiver_acc,
                    amount=amount,
                    transaction_type="transfer"
                )

            return Response({"message": "Transfer successful", "balance": sender_acc.balance})
        except Account.DoesNotExist:
            return Response({"error": "Receiver account not found"}, status=status.HTTP_404_NOT_FOUND)

class TransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(
            Q(from_account=account) | Q(to_account=account)
        ).order_by('-timestamp')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)