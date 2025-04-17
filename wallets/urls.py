from django.urls import path

from wallets.apps import WalletsConfig
from wallets.views import WalletCreateView, WalletOperationView, WalletDetailView

app_name = WalletsConfig.name

urlpatterns = [
    path('create/', WalletCreateView.as_view()),
    path('<uuid:wallet_uuid>/operation/', WalletOperationView.as_view()),
    path('<uuid:wallet_uuid>/', WalletDetailView.as_view()),
]
