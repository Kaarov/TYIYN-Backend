from rest_framework import routers

from .views import BudgetModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=BudgetModelViewSet, basename="budget")

urlpatterns = []

urlpatterns += router.urls
