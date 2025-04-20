from django.urls import path

from .views import TransferListCreateAPIView

urlpatterns = [
    path("", TransferListCreateAPIView.as_view(), name="transfer"),
]
