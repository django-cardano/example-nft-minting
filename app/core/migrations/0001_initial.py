# Generated by Django 3.2.3 on 2021-05-26 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cardano.fields
import django_cardano.models
import django_cardano.storage
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.DJANGO_CARDANO_TRANSACTION_MODEL),
        migrations.swappable_dependency(settings.DJANGO_CARDANO_MINTING_POLICY_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('payment_address', django_cardano.fields.CardanoAddressField(max_length=200)),
                ('payment_signing_key', models.FileField(max_length=200, storage=django_cardano.storage.CardanoDataStorage, upload_to=django_cardano.models.file_upload_path)),
                ('payment_verification_key', models.FileField(max_length=200, storage=django_cardano.storage.CardanoDataStorage, upload_to=django_cardano.models.file_upload_path)),
                ('stake_address', django_cardano.fields.CardanoAddressField(max_length=200)),
                ('stake_signing_key', models.FileField(max_length=200, storage=django_cardano.storage.CardanoDataStorage, upload_to=django_cardano.models.file_upload_path)),
                ('stake_verification_key', models.FileField(max_length=200, storage=django_cardano.storage.CardanoDataStorage, upload_to=django_cardano.models.file_upload_path)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django_cardano.models.WalletManager()),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('image', models.ImageField(upload_to='')),
                ('minting_policy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.DJANGO_CARDANO_MINTING_POLICY_MODEL)),
                ('minting_transaction', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.DJANGO_CARDANO_TRANSACTION_MODEL)),
            ],
        ),
    ]
