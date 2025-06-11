from django.urls import path
from rest_framework import routers

from .views import IncomeCardIdAPIView, IncomeModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=IncomeModelViewSet, basename="income")

urlpatterns = [
    path("card-id/", IncomeCardIdAPIView.as_view(), name="income-card-id"),
]

urlpatterns += router.urls
