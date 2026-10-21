from django.urls import path
from .views import (
    AccountView,
    DepositView,
    LoginView,
    ProfileView,
    RegisterView,
    TransactionView,
    TransferView,
    WithdrawView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('account/', AccountView.as_view(), name='account'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
]