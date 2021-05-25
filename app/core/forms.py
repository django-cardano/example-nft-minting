from django import forms
from django.core.exceptions import ValidationError

from django_cardano.models import get_wallet_model
from django_cardano.validators import validate_cardano_address

Wallet = get_wallet_model()



TEXT_INPUT_CLASSES = """
    mt-1 rounded-md border-gray-300 shadow-sm
    focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50
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
        label='Receiving Address',
        widget=forms.Textarea(attrs={
            'class': TEXT_INPUT_CLASSES,
            'placeholder': 'Paste an address...',
            'rows': 4,
        }),
        validators=(validate_cardano_address,)
    )
    amount = forms.CharField(
        label='Amount of ADA to send',
        widget=forms.NumberInput(attrs={
            'class': TEXT_INPUT_CLASSES,
            'step': 'any',
        }),
    )
    password = forms.CharField(
        label='Spending password',
        widget=forms.PasswordInput(attrs={
            'class': TEXT_INPUT_CLASSES,
        }),
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return int(amount) * 1000000