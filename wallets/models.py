import uuid
from django.db import models

class Wallet(models.Model):
    """
    Модель кошелька
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"


class Operation(models.Model):
    """
    Модель операций
    """
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    OPERATION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw'),
    ]
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='operations'
    )
    operation_type = models.CharField(
        max_length=8,
        choices=OPERATION_TYPES
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )