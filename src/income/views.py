from rest_framework import permissions, viewsets

from .models import IncomeModel
from .serializers import IncomeSerializer


class IncomeModelViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return IncomeModel.objects.filter(user=self.request.user).order_by("created_at")

    def perform_destroy(self, instance):
        instance.card.balance -= instance.amount
        instance.card.save()
        instance.delete()
