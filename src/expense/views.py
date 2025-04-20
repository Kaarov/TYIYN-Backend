from rest_framework import viewsets

from .models import ExpenseModel
from .serializers import ExpenseSerializer


class ExpenseModelViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return ExpenseModel.objects.filter(user=self.request.user).order_by("created_at")

    def perform_destroy(self, instance):
        instance.card.balance -= instance.amount
        instance.card.save()
        instance.delete()
