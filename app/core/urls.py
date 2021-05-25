from django.urls import path

from . import views

urlpatterns = [
    path('wallets/', views.WalletListView.as_view(), name='wallet.list'),
    path('wallet/<uuid:pk>/', views.WalletDetailView.as_view(), name='wallet.read'),
    path('transaction/<str:tx_id>', views.TransactionDetailView.as_view(), name='transaction.read'),
    path('query/tip/', views.QueryTipView.as_view(), name='query.tip'),
]
