from django.contrib import admin

from django_cardano.models import (
    get_minting_policy_model,
    get_transaction_model,
    get_wallet_model,
)

from .forms import WalletCreateForm

MintingPolicy = get_minting_policy_model()
Transaction = get_transaction_model()
Wallet = get_wallet_model()


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_address', 'id',)
    fields = ('name',)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return WalletCreateForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj:
            return ('name', 'password',)

        return super().get_fields(request, obj)
