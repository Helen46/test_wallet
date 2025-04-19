from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@example.com', is_staff=True, is_superuser=True, )
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """ Тест создания пользователя"""
        url = reverse('users:register')
        data = {
            'email': 'test@example.com',
            'password': 'qwe123',
            'first_name': 'Jon',
            'last_name': 'Snow'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.all().count(), 2
        )

    def test_user_retrieve(self):
        """ Тест просмотра пользователя"""
        url = reverse('users:user_retrieve', args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('email'), self.user.email
        )

    def test_user_list(self):
        """Тест просмотра списка пользователей"""
        url = reverse('users:users_list')
        response = self.client.get(url)
        result = [
            {
                'email': self.user.email,
                'first_name': '',
                'id': self.user.id,
                'last_name': '',
                'password': '',
                'phone': None
            }
        ]
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_user_update(self):
        """ Тест изменения пользователя"""
        url = reverse('users:user_update', args=(self.user.pk,))
        data = {
            'last_name': 'Targaryen',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('last_name'), 'Targaryen'
        )

    def test_user_delete(self):
        """ Тест удаления пользователя"""
        url = reverse('users:user_delete', args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            User.objects.all().count(), 0
        )
