from django.views.generic import (
    DetailView,
    ListView,
)
from .models import Wallet


class WalletListView(ListView):
    model = Wallet


class WalletDetailView(DetailView):
    model = Wallet

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
