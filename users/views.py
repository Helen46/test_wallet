from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsAdmin, IsYourObject
from users.serializers import UserSerializer, UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Создание пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """
    Список пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


class UserRetrieveApiView(RetrieveAPIView):
    """
    Просмотр пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsYourObject,)


class UserUpdateApiView(UpdateAPIView):
    """
    Изменение пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsYourObject,)


class UserDestroyApiView(DestroyAPIView):
    """
    Удаление пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsYourObject,)
