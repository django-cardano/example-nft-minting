from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError

from django_cardano.models import get_wallet_model
from django_cardano.validators import validate_cardano_address

Wallet = get_wallet_model()

TEXT_INPUT_CLASSES = """
    mt-1 rounded-md border-gray-300 shadow-sm text-gray-700
    focus:border-green-700 focus:ring focus:ring-green-600 focus:ring-opacity-25
"""


class WalletCreateForm(forms.ModelForm):
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Wallet
        fields = ('name', 'password',)


class TransferADAForm(forms.Form):
    address = forms.CharField(
        label='Receiving address',
        widget=forms.Textarea(attrs={
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Paste an address...',
            'rows': 4,
        }),
        validators=(validate_cardano_address,)
    )

    quantity = forms.CharField(
        label='Amount of ADA to send',
        widget=forms.NumberInput(attrs={
            'class': TEXT_INPUT_CLASSES,
            'step': 'any',
        }),
    )

    fee = forms.CharField(
        label='Transaction fee',
        widget=forms.TextInput(attrs={
            'class': TEXT_INPUT_CLASSES + 'bg-gray-50',
            'disabled': True,
            'value': '--------',
        }),
        required=False,
    )
    password = forms.CharField(
        label='Spending password',
        widget=forms.PasswordInput(attrs={
            'class': TEXT_INPUT_CLASSES,
        }),
        required=False,
    )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        return int(Decimal(quantity) * 1000000)


class MintNFTForm(forms.Form):
    payment_wallet = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        widget=forms.Select(
            attrs={'class': TEXT_INPUT_CLASSES},
        )
    )

    address = forms.CharField(
        label='Receiving address',
        widget=forms.Textarea(attrs={
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Paste an address...',
            'rows': 4,
        }),
        validators=(validate_cardano_address,)
    )

    fee = forms.CharField(
        label='Transaction fee',
        widget=forms.TextInput(attrs={
            'class': TEXT_INPUT_CLASSES + 'bg-gray-50',
            'disabled': True,
            'value': '--------',
        }),
        required=False,
    )
    password = forms.CharField(
        label='Spending password',
        widget=forms.PasswordInput(attrs={
            'class': TEXT_INPUT_CLASSES,
        }),
        required=False,
    )
