from django.contrib import admin

from wallets.models import Wallet, Operation


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'balance',)


@admin.register(Operation )
class OperationAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'operation_type', 'amount', 'created_at')
