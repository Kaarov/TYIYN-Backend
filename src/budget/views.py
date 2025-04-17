from rest_framework import viewsets

from .models import BudgetModel
from .serializers import BudgetListSerializer, BudgetSerializer


class BudgetModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return BudgetModel.objects.filter(user=self.request.user).order_by("created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return BudgetListSerializer
        return BudgetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
