from django.views.generic import RedirectView
from django.urls import path

from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='wallet.list')),

    path('wallets/', views.WalletListView.as_view(), name='wallet.list'),
    path('wallet/<uuid:pk>/', views.WalletDetailView.as_view(), name='wallet.read'),

    path('assets/', views.AssetListView.as_view(), name='asset.list'),
    path('asset/<uuid:pk>/', views.AssetDetailView.as_view(), name='asset.read'),

    path('transaction/<str:tx_id>', views.TransactionDetailView.as_view(), name='transaction.read'),
    path('query/tip/', views.QueryTipView.as_view(), name='query.tip'),
]
