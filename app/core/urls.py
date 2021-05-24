from django.urls import path

from .views import (
    WalletListView,
    WalletDetailView,
)

urlpatterns = [
    path('wallets/', WalletListView.as_view(), name='wallet.list'),
    path('wallet/<uuid:pk>/', WalletDetailView.as_view(), name='wallet.read'),
]
