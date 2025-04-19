from django.urls import path

from wallets.apps import WalletsConfig
from wallets.views import WalletCreateView, WalletOperationView, WalletRetrieveView, WalletDestroyApiView

app_name = WalletsConfig.name

urlpatterns = [
    path('create/', WalletCreateView.as_view(), name='wallet_create'),
    path('<uuid:wallet_uuid>/operation/', WalletOperationView.as_view(), name='wallet_operation'),
    path('<uuid:wallet_uuid>/', WalletRetrieveView.as_view(), name='wallet_retrieve'),
    path('<uuid:uuid>/destroy/', WalletDestroyApiView.as_view(), name='wallet_destroy'),
]
