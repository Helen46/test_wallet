from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError

from wallets.models import Wallet, Operation
from wallets.serializers import OperationSerializer, WalletSerializer, WalletCreateSerializer


class WalletCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WalletCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'wallets_wallet_owner_id_key' in str(e):
                    return Response(
                        {"detail": "У пользователя уже есть кошелек."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                raise
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletOperationView(APIView):
    def post(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = OperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        op_type = serializer.validated_data['operation_type']
        amount = serializer.validated_data['amount']

        with transaction.atomic():
            if op_type == Operation.DEPOSIT:
                wallet.balance += amount
            elif op_type == Operation.WITHDRAW:
                if wallet.balance < amount:
                    return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
                wallet.balance -= amount
            wallet.save()
            Operation.objects.create(wallet=wallet, operation_type=op_type, amount=amount)
        return Response({'balance': wallet.balance}, status=status.HTTP_200_OK)


class WalletDetailView(APIView):
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
