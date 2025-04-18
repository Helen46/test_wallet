from django.contrib import admin

from wallets.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'balance',)
