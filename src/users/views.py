from rest_framework import generics

from .models import User
from .serializers import UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(username=self.request.user.username)
