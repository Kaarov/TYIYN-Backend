from django.db.models import Sum
from django.db.models.functions import ExtractMonth, TruncDay
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from expense.models import ExpenseModel
from income.models import IncomeModel


@extend_schema(
    summary="Get Bar Chart data",
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
class BarChartDataAPIView(APIView):
    def get(self, request):
        operation_type = request.query_params.get("type")
        month = request.query_params.get("month", "ALL")
        year = request.query_params.get("year", "ALL")
        card_id = request.query_params.get("card")
        detailed = request.query_params.get("detailed", "false").lower() == "true"

        MONTHS = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        if operation_type == "income":
            model = IncomeModel
        elif operation_type == "expense":
            model = ExpenseModel
        else:
            return Response({"error": "the type should be 'income' or 'expense'"}, status=400)

        queryset = model.objects.filter(user=request.user)

        if card_id:
            queryset = queryset.filter(card_id=card_id)

        group_by_day = True
        if year.lower() != "all":
            queryset = queryset.filter(date__year=int(year))
        else:
            group_by_day = False

        if month.lower() != "all":
            try:
                month_int = int(month)
                if not 1 <= month_int <= 12:
                    raise ValueError()
                queryset = queryset.filter(date__month=month_int)
            except ValueError:
                return Response({"error": "month must be from 1 to 12 or 'ALL'"}, status=400)
        else:
            group_by_day = False

        if detailed:
            data = queryset.values("date", "category").annotate(total=Sum("amount")).order_by("date")
            result = [{"date": item["date"], "category": item["category"], "total": item["total"]} for item in data]
            return Response(result)

        if group_by_day:
            data = (
                queryset.annotate(day=TruncDay("date"))
                .values("day", "category")
                .annotate(total=Sum("amount"))
                .order_by("day")
            )
            result = [{"date": item["day"], "category": item["category"], "total": item["total"]} for item in data]
        else:
            data = (
                queryset.annotate(month=ExtractMonth("date"))
                .values("month", "category")
                .annotate(total=Sum("amount"))
                .order_by("month")
            )
            result = [
                {
                    "month": MONTHS.get(item["month"], str(item["month"])),
                    "category": item["category"],
                    "total": item["total"],
                }
                for item in data
            ]

        return Response(result)
