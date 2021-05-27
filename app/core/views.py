from django.http import Http404
from django.http import JsonResponse
from django.views.generic import (
    View,
    DetailView,
    FormView,
    ListView,
)
from django.urls import reverse
from django.utils.translation import gettext as _

from django_cardano.exceptions import CardanoError, CardanoErrorType
from django_cardano.models import (
    get_transaction_model,
    get_wallet_model,
)
from django_cardano.util import CardanoUtils

from .forms import (
    ConsolidateTokensForm,
    MintNFTForm,
    TransferADAForm,
)
from .models import Asset
from .shortcuts import clean_token_asset_name

Transaction = get_transaction_model()
Wallet = get_wallet_model()


class AssetListView(ListView):
    model = Asset


class AssetDetailView(FormView):
    form_class = MintNFTForm
    template_name = 'core/asset_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset'] = Asset.objects.get(pk=self.kwargs['pk'])
        return context

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction = None

    def form_valid(self, form):
        asset = Asset.objects.get(pk=self.kwargs['pk'])

        form_data = form.cleaned_data

        policy = form_data['minting_policy']
        payment_wallet = form_data['payment_wallet']
        to_address = form_data['destination_address']
        spending_password = form_data['spending_password']
        minting_password = form_data['minting_password']

        asset_name = clean_token_asset_name(asset.name)
        tx_metadata = {
            "721": {
                policy.policy_id: {
                    asset_name: asset.metadata
                }
            }
        }
        mint_tokens_kwargs = {
            'policy': policy,
            'quantity': 1,
            'to_address': to_address,
            'metadata': tx_metadata,
            'asset_name': asset_name,
        }

        if spending_password and minting_password:
            try:
                self.transaction = payment_wallet.mint_tokens(
                    **mint_tokens_kwargs,
                    spending_password=spending_password,
                    minting_password=minting_password,
                )
                asset.minting_transaction = self.transaction
                asset.minting_policy = policy
                asset.save()

                return super().form_valid(form)
            except CardanoError as e:
                error_field_name = None
                if e.code == CardanoErrorType.SIGNING_KEY_DECRYPTION_FAILURE:
                    error_field_name = 'spending_password'
                elif e.code == CardanoErrorType.POLICY_SIGNING_KEY_DECRYPTION_FAILURE:
                    error_field_name = 'minting_password'
                form.add_error(error_field_name, str(e))
                return self.form_invalid(form)
        else:
            try:
                transaction = payment_wallet.mint_tokens(
                    **mint_tokens_kwargs,
                    spending_password=None,
                    minting_password=None,
                )
                tx_fee = transaction.calculate_min_fee()
                return JsonResponse({'fee': tx_fee})
            except CardanoError as e:
                return JsonResponse({'error': str(e)}, status=400)

    def get_success_url(self):
        return reverse('transaction.read', kwargs={
            'tx_id': self.transaction.tx_id
        })


class WalletListView(ListView):
    model = Wallet


class WalletDetailView(FormView):
    form_class = TransferADAForm
    template_name = 'core/wallet_detail.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction = None

    def get_success_url(self):
        return reverse('transaction.read', kwargs={
            'tx_id': self.transaction.tx_id
        })

    def form_valid(self, form):
        form_data = form.cleaned_data

        wallet = Wallet.objects.get(pk=self.kwargs['pk'])
        to_address = form_data['address']
        quantity = form_data['quantity']
        spending_password = form_data['spending_password']

        if spending_password:
            try:
                self.transaction = wallet.send_lovelace(
                    to_address=to_address,
                    quantity=quantity,
                    password=spending_password,
                )
                return super().form_valid(form)
            except CardanoError as e:
                error_field_name = None
                if e.code == CardanoErrorType.SIGNING_KEY_DECRYPTION_FAILURE:
                    error_field_name = 'spending_password'
                form.add_error(error_field_name, str(e))
                return self.form_invalid(form)
        else:
            try:
                transaction = wallet.send_lovelace(
                    to_address=to_address,
                    quantity=quantity,
                )
                tx_fee = transaction.calculate_min_fee()
                return JsonResponse({'fee': tx_fee})
            except CardanoError as e:
                return JsonResponse({'error': str(e)}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'wallet': Wallet.objects.get(pk=self.kwargs['pk']),
            'consolidate_tokens_form': ConsolidateTokensForm(),
        })

        return context


class WalletConsolidateView(FormView):
    form_class = ConsolidateTokensForm

    def form_valid(self, form):
        wallet = Wallet.objects.get(pk=self.kwargs['pk'])
        try:
            transaction = wallet.consolidate_utxos(
                password=form.cleaned_data['consolidate_tokens_password']
            )
        except CardanoError as e:
            return JsonResponse({'error': str(e)}, status=400)

        transaction_url = reverse('transaction.read', kwargs={
            'tx_id': transaction.tx_id
        })
        return JsonResponse({'transaction_url': transaction_url})

    def form_invalid(self, form):
        return JsonResponse({'error': 'Invalid password'})


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'core/transaction_detail.html'

    def get_object(self, queryset=None):
        try:
            # Get the single item from the filtered queryset
            return self.get_queryset().get(tx_id=self.kwargs.get('tx_id'))
        except Transaction.DoesNotExist:
            raise Http404(_("No transaction found matching the query"))


class QueryTipView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(CardanoUtils.query_tip())
