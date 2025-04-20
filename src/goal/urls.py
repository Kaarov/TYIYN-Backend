from rest_framework import routers

from .views import GoalModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=GoalModelViewSet, basename="goal")

urlpatterns = []

urlpatterns += router.urls
