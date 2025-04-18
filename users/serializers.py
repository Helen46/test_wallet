from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор модели User
    """
    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(ModelSerializer):
    """
    Сериализатор просмотра пользователя
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone')
