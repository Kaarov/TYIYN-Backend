from django.db.models import Sum
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import CategoryModel
from expense.models import ExpenseModel
from income.models import IncomeModel


@extend_schema(
    summary="Get Pie Chart data",
    description=(
        "This endpoint returns aggregated expenses or income by category. "
        "It can be filtered by type (income/expense), month, year, and card. "
        "If detailed=true is specified, a detailed list of transactions is returned."
    ),
    parameters=[
        OpenApiParameter(name="type", required=True, type=str, description="Operation type: 'income' or 'expense'"),
        OpenApiParameter(name="month", required=False, type=str, description="Month number (1-12) or 'all'"),
        OpenApiParameter(name="year", required=False, type=str, description="Year, for example: '2025' or 'all'"),
        OpenApiParameter(name="card_id", required=True, type=int, description="ID card"),
        OpenApiParameter(
            name="detailed", required=False, type=bool, description="If true, returns the full list of transactions."
        ),
    ],
    responses={200: None},
)
class PieChartDataAPIView(APIView):
    def get(self, request):
        user = request.user
        type_ = request.query_params.get("type")  # income / expense
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        card_id = request.query_params.get("card_id")

        if type_ not in ["income", "expense"]:
            return Response({"detail": "Type must be 'income' or 'expense'"}, status=400)

        Model = IncomeModel if type_ == "income" else ExpenseModel

        queryset = Model.objects.filter(user=user)

        if card_id:
            queryset = queryset.filter(card_id=card_id)

        if month and month.lower() != "all":
            queryset = queryset.filter(date__month=int(month))

        if year and year.lower() != "all":
            queryset = queryset.filter(date__year=int(year))

        grouped_data = queryset.values("category").annotate(total=Sum("amount")).order_by("-total")

        if request.query_params.get("detailed") == "true":
            details = queryset.values("description", "amount", "date", "category").order_by("-date")

            return Response(list(details))

        detailed = [
            {
                "category": entry["category"],
                "category_title": CategoryModel.objects.get(id=entry["category"]).get_name(user.language),
                "total": float(entry["total"]),
            }
            for entry in grouped_data
        ]

        return Response(detailed)
