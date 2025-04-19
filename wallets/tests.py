from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from wallets.models import Wallet
from users.models import User


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class WalletTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test1@example.com',
            password='qwe123',
            first_name='Jon',
            last_name='Snow'
        )
        self.admin = User.objects.create(
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        self.client.force_authenticate(user=self.user)

    def test_create_wallet_success(self):
        """Тест успешного создания кошелька"""
        url = reverse('wallets:wallet_create')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)

    def test_create_wallet_duplicate(self):
        """Тест создания второго кошелька для пользователя"""
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000.00)
        url = reverse('wallets:wallet_create')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Декодируем ответ и проверяем сообщение
        response_content = response.content.decode('utf-8')
        self.assertIn('У пользователя уже есть кошелек', response_content)

    def test_retrieve_wallet_as_owner(self):
        """Тест получения кошелька владельцем"""
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000.00)
        self.client.force_authenticate(user=self.user)
        url = reverse('wallets:wallet_retrieve', args=[self.wallet.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uuid'], str(self.wallet.uuid))

    def test_retrieve_wallet_as_admin(self):
        """Тест получения кошелька администратором"""
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000.00)
        self.client.force_authenticate(user=self.admin)
        url = reverse('wallets:wallet_retrieve', args=[self.wallet.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_wallet_unauthorized(self):
        """Тест доступа к чужому кошельку"""
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000.00)
        other_user =User.objects.create(
            email='test2@example.com',
            password='qwe123',
            first_name='Daenerys',
            last_name='Targaryen'
        )
        self.client.force_authenticate(user=other_user)
        url = reverse('wallets:wallet_retrieve', args=[self.wallet.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wallet_success(self):
        """Тест успешного удаления кошелька"""
        self.wallet = Wallet.objects.create(owner=self.user, balance=0.00)
        url = reverse('wallets:wallet_destroy', args=[self.wallet.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_delete_wallet_with_balance(self):
        """Тест удаления кошелька с положительным балансом"""
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000.00)
        url = reverse('wallets:wallet_destroy', args=[self.wallet.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertIn('Нельзя удалить кошелек с положительным балансом', response_content)


class OperationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test1@example.com',
            password='qwe123',
            first_name='Jon',
            last_name='Snow'
        )
        self.wallet = Wallet.objects.create(owner=self.user, balance=1000.00)
        self.client.force_authenticate(user=self.user)

    def test_deposit_operation(self):
        """Тест успешного пополнения баланса"""
        url = reverse('wallets:wallet_operation', args=[self.wallet.uuid])
        data = {'operation_type': 'DEPOSIT', 'amount': '500.00'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 1500.00)

    def test_withdraw_success(self):
        """Тест успешного списания средств"""
        url = reverse('wallets:wallet_operation', args=[self.wallet.uuid])
        data = {'operation_type': 'WITHDRAW', 'amount': '500.00'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 500.00)

    def test_withdraw_insufficient_funds(self):
        """Тест списания при недостатке средств"""
        url = reverse('wallets:wallet_operation', args=[self.wallet.uuid])
        data = {'operation_type': 'WITHDRAW', 'amount': '1500.00'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertIn('Недостаточно средств', response_content)

    def test_invalid_operation_type(self):
        """Тест невалидного типа операции"""
        url = reverse('wallets:wallet_operation', args=[self.wallet.uuid])
        data = {'operation_type': 'INVALID', 'amount': '500.00'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_amount(self):
        """Тест отрицательной суммы операции"""
        url = reverse('wallets:wallet_operation', args=[self.wallet.uuid])
        data = {'operation_type': 'DEPOSIT', 'amount': '-500.00'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
