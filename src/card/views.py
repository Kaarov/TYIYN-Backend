from rest_framework import viewsets

from .models import CardModel
from .serializers import CardListSerializer, CardSerializer


class CardModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return CardModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return CardListSerializer
        return CardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
