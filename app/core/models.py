from django.conf import settings
from django.db import models

from django_cardano.models import (
    AbstractMintingPolicy,
    AbstractTransaction,
    AbstractWallet,
)


# Swap these classes initially so they may be easily extended later if necessary
class MintingPolicy(AbstractMintingPolicy):
    pass


class Transaction(AbstractTransaction):
    pass


class Wallet(AbstractWallet):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


# -----------------------------------------------------------------------------
class Asset(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    metadata = models.JSONField(default=dict)

    minting_policy = models.ForeignKey(
        settings.DJANGO_CARDANO_MINTING_POLICY_MODEL,
        blank=True, null=True,
        on_delete=models.PROTECT
    )
    minting_transaction = models.OneToOneField(
        settings.DJANGO_CARDANO_TRANSACTION_MODEL,
        blank=True, null=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.metadata.get('name', f'Asset {self.id}')
