from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from wallets.models import Operation, Wallet


class WalletSerializer(ModelSerializer):
    """
    Сериализатор модели Wallet
    """
    class Meta:
        model = Wallet
        fields = ('uuid', 'balance', 'owner')
        read_only_fields = ('balance', 'created_at')


class WalletCreateSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('uuid', 'balance')
        read_only_fields = ('wallet', 'created_at')

    def create(self, validated_data):
        # Добавляем текущего пользователя в данные для сохранения
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class OperationSerializer(ModelSerializer):
    """
    Сериализатор для операций
    """
    class Meta:
        model = Operation
        fields = ('operation_type', 'amount')

    def validate_amount(self, value):
        """
        Базовая проверка: сумма > 0 для всех операций
        """
        if value <= 0:
            raise serializers.ValidationError('Сумма должна быть положительной')
        return value
