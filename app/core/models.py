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
    pass
