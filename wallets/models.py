import uuid
from decimal import Decimal

from django.db import models, transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from config.settings import AUTH_USER_MODEL


class Wallet(models.Model):
    """
    Модель кошелька
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID кошелька'
    )
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name='Баланс кошелька'
    )
    owner = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name='Владелец кошелька'
    )

    @transaction.atomic
    def update_balance(self, operation_type: str, amount: Decimal):
        """Обновление баланса с проверкой типа операции"""
        # Блокировка записи
        wallet = Wallet.objects.select_for_update().get(pk=self.pk)

        # Проверка для списания
        if operation_type == 'WITHDRAW' and wallet.balance < amount:
            raise ValidationError('Недостаточно средств')

        # Определение дельты
        delta = amount if operation_type == 'DEPOSIT' else -amount

        # Атомарное обновление
        Wallet.objects.filter(pk=self.pk).update(
            balance=F('balance') + delta
        )
        self.refresh_from_db()

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'


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
        related_name='operations',
        verbose_name='Кошелек'
    )
    operation_type = models.CharField(
        max_length=8,
        choices=OPERATION_TYPES,
        verbose_name='Тип операции'
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Сумма операции'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время операции'
    )

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'