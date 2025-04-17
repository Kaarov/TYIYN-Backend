from rest_framework import routers

from .views import CategoryModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=CategoryModelViewSet, basename="category")

urlpatterns = []

urlpatterns += router.urls
