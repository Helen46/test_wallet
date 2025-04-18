from decimal import Decimal

from rest_framework import serializers
from rest_framework.fields import ChoiceField, DecimalField
from rest_framework.serializers import ModelSerializer

from wallets.models import Operation, Wallet


class OperationSerializer(serializers.Serializer):
    """
    Сериализатор для операций
    """
    # дополнительная валидация для поля operation_type
    operation_type = ChoiceField(
        choices=Operation.OPERATION_TYPES
    )
    # дополнительная валидация для поля amount и добавление минимального значения
    amount = DecimalField(
        max_digits=20,
        decimal_places=2,
        min_value=Decimal('0.01')
    )


class WalletSerializer(ModelSerializer):
    """
    Сериализатор модели Wallet
    """
    class Meta:
        model = Wallet
        fields = ('uuid', 'balance')


class WalletCreateSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['uuid', 'balance']

    def create(self, validated_data):
        # Добавляем текущего пользователя в данные для сохранения
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
