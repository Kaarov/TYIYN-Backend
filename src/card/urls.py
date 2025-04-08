from rest_framework import routers

from .views import CardModelViewSet

router = routers.DefaultRouter()
router.register("", viewset=CardModelViewSet, basename="card")

urlpatterns = []

urlpatterns += router.urls
