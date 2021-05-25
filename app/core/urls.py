from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    TransactionDetailView,
    WalletListView,
    WalletDetailView,
)

urlpatterns = [
    path('wallets/', WalletListView.as_view(), name='wallet.list'),
    path('wallet/<uuid:pk>/', WalletDetailView.as_view(), name='wallet.read'),
    path('transaction/<str:tx_id>', TransactionDetailView.as_view(), name='transaction.read'),
]
