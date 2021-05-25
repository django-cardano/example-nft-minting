from django.contrib import admin

from django_cardano.models import (
    get_minting_policy_model,
    get_transaction_model,
    get_wallet_model,
)

from .forms import WalletCreateForm
from .models import Asset

MintingPolicy = get_minting_policy_model()
Transaction = get_transaction_model()
Wallet = get_wallet_model()


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_address', 'lovelace_balance',)
    search_fields = ('name', 'payment_address',)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return WalletCreateForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if not obj:
            return ('name', 'password',)
        return ('name',)

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        wallet = form.save(commit=False)

        if not change:
            wallet.generate_keys(form.cleaned_data['password'])
            wallet.creator = request.user

        return wallet


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'metadata', 'id',)
    fields = ('name', 'image', 'metadata',)
