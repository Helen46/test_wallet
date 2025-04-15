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