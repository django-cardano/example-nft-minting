from django.http import Http404, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.generic import (
    View,
    DetailView,
    FormView,
    ListView,
)
from django.urls import reverse
from django.utils.translation import gettext as _

from django_cardano.exceptions import CardanoError
from django_cardano.models import (
    get_transaction_model,
    get_wallet_model,
)
from django_cardano.util import CardanoUtils

from .forms import TransferADAForm

Transaction = get_transaction_model()
Wallet = get_wallet_model()


class WalletListView(ListView):
    model = Wallet


class WalletDetailView(FormView):
    form_class = TransferADAForm
    model = Wallet
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
        spending_password = form_data['password']

        if spending_password:
            try:
                self.transaction = wallet.send_lovelace(
                    to_address=to_address,
                    quantity=quantity,
                    password=spending_password
                )
            except CardanoError as e:
                form.add_error(None, str(e))
                return self.form_invalid(form)

            return super().form_valid(form)
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
        context['wallet'] = Wallet.objects.get(pk=self.kwargs['pk'])
        return context


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'core/transaction_complete.html'

    def get_object(self, queryset=None):
        try:
            # Get the single item from the filtered queryset
            return self.get_queryset().get(tx_id=self.kwargs.get('tx_id'))
        except Transaction.DoesNotExist:
            raise Http404(_("No transaction found matching the query"))


class QueryTipView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(CardanoUtils.query_tip())
