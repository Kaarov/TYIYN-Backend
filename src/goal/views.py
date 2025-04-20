from rest_framework import viewsets

from .models import GoalModel
from .serializers import GoalListSerializer, GoalSerializer


class GoalModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return GoalModel.objects.filter(user=self.request.user).order_by("created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return GoalListSerializer
        return GoalSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
