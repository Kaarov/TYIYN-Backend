from django.db import models
from django.db.models import Case, Value, When, F
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views, viewsets
from rest_framework.response import Response

from .models import IncomeModel
from .serializers import IncomeSerializer


@extend_schema(
    summary="Get Incomes by card id",
    description=("This endpoint returns incomes by card id. "),
    parameters=[
        OpenApiParameter(name="card_id", required=True, type=int, description="ID card"),
        OpenApiParameter(
            name="detailed", required=False, type=bool, description="If true, returns the full list of transactions."
        ),
    ],
    responses={200: None},
)
class IncomeCardIdAPIView(views.APIView):
    def get(self, request):
        user = request.user
        card_id = request.query_params.get("card_id")

        queryset = IncomeModel.objects.filter(user=user, card_id=card_id)

        category_title_expression = Case(
            When(category__isnull=True, then=Value(None)),
            When(user__language='en', then=F('category__title_en')),
            When(user__language='ru', then=F('category__title_ru')),
            When(user__language='ky', then=F('category__title_ky')),
            default=F('category__title_en'),  # Fallback
            output_field=models.CharField()
        )

        details = queryset.annotate(
            category_title=category_title_expression
        ).values(
            "id",
            "created_at",
            "updated_at",
            "amount",
            "description",
            "date",
            "card",
            "category",
            "user",
            "category_title",  # This is the key
        ).order_by("-created_at")

        return Response(list(details))


class IncomeModelViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return IncomeModel.objects.filter(user=self.request.user).order_by("created_at")

    def perform_destroy(self, instance):
        instance.card.balance -= instance.amount
        instance.card.save()
        instance.delete()
