from django import forms

from django_cardano.models import get_wallet_model

Wallet = get_wallet_model()


class WalletCreateForm(forms.ModelForm):
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Wallet
        fields = ('name', 'password',)
