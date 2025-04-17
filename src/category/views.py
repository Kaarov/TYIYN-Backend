from rest_framework import viewsets

from .models import CategoryModel
from .serializers import (
    CategoryCreateSerializer,
    CategoryListSerializer,
    CategorySerializer,
)


class CategoryModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return CategoryModel.objects.filter(user=self.request.user).order_by("created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "create":
            return CategoryCreateSerializer
        return CategorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
