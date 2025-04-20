from rest_framework import routers

from .views import IncomeModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=IncomeModelViewSet, basename="income")

urlpatterns = []

urlpatterns += router.urls
