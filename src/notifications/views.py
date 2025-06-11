from rest_framework import generics
from rest_framework.response import Response

from .models import NotificationModel
from .serializers import NotificationSerializer


class NotificationListAPIView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):  # noqa A003
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def get_queryset(self):
        return NotificationModel.objects.filter(user=self.request.user).order_by("created_at")

    def get_serializer_class(self):
        return NotificationSerializer
