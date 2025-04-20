from rest_framework import generics, status
from rest_framework.response import Response

from .models import TransferModel
from .serializers import TransferCreateSerializer, TransferListSerializer


class TransferListCreateAPIView(generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):  # noqa A003
        transfers = TransferModel.objects.filter(user=request.user).order_by("created_at")
        serializer = self.get_serializer(transfers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            transfer = serializer.save(user=request.user)
            return Response(self.get_serializer(transfer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TransferCreateSerializer
        elif self.request.method == "GET":
            return TransferListSerializer
