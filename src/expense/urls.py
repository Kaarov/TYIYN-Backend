from rest_framework import routers

from .views import ExpenseModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=ExpenseModelViewSet, basename="expense")

urlpatterns = []

urlpatterns += router.urls
