"""
URL configuration for bankcore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
    RegisterView, LoginView, ProfileView, AccountView, 
    DepositView, WithdrawView, TransferView, TransactionView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/account/', AccountView.as_view(), name='account'),
    path('api/deposit/', DepositView.as_view(), name='deposit'),
    path('api/withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('api/transfer/', TransferView.as_view(), name='transfer'),
    path('api/transactions/', TransactionView.as_view(), name='transactions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)