from django.urls import path
from rest_framework import routers

from .views import ExpenseCardIdAPIView, ExpenseModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=ExpenseModelViewSet, basename="expense")

urlpatterns = [
    path("card-id/", ExpenseCardIdAPIView.as_view(), name="expense-card-id"),
]

urlpatterns += router.urls
