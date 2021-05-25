from django.http import Http404
from django.utils.translation import gettext as _

from django.views.generic import (
    DetailView,
    FormView,
    ListView,
)
from django.urls import reverse

from django_cardano.exceptions import CardanoError
from django_cardano.models import (
    get_transaction_model,
    get_wallet_model,
)

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
        try:
            self.transaction = wallet.send_lovelace(
                to_address=form_data['address'],
                quantity=form_data['amount'],
                password=form_data['password']
            )
        except CardanoError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)

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
