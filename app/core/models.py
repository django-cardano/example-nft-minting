import json
import uuid

from django.conf import settings
from django.db import models

from django_cardano.models import (
    AbstractMintingPolicy,
    AbstractTransaction,
    AbstractWallet,
)

from django_cardano.settings import django_cardano_settings

lovelace_unit = django_cardano_settings.LOVELACE_UNIT


class Wallet(AbstractWallet):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} (₳ {self.ada_balance})'

    @property
    def lovelace_balance(self):
        lovelace_balance = sum([utxo['Tokens'][lovelace_unit] for utxo in self.lovelace_utxos])
        return lovelace_balance if lovelace_balance else 0

    @property
    def ada_balance(self):
        return self.lovelace_balance / 1000000


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    metadata = models.JSONField(default=dict, blank=True)
    image = models.ImageField()

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
        return self.name

    @property
    def metadata_json(self):
        return json.dumps(self.metadata)
