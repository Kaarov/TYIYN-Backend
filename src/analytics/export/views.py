from datetime import datetime

import pandas as pd
from django.http import HttpResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.views import APIView

from expense.models import ExpenseModel
from income.models import IncomeModel


@extend_schema(
    summary="Export operations (income/expenses)",
    description="Allows you to export income or expenses in JSON or Excel format with date and map filtering.",
    parameters=[
        OpenApiParameter(name="type", description="Type of operation: `income` or `expense`", required=True, type=str),
        OpenApiParameter(name="format", description="File format: `json` or `xlsx`", required=True, type=str),
        OpenApiParameter(name="month", description="Month (1-12 or 'all')", type=str, required=False),
        OpenApiParameter(name="year", description="Year (for example, 2025 or 'all')", type=str, required=False),
        OpenApiParameter(name="card", description="Card ID (optional)", type=int, required=False),
    ],
)
class ExportOperationsAPIView(APIView):
    def get(self, request):
        operation_type = request.query_params.get("type", "").lower()
        export_format = request.query_params.get("format", "json").lower()
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        card_id = request.query_params.get("card")

        if operation_type == "expense":
            Model = ExpenseModel
        elif operation_type == "income":
            Model = IncomeModel
        else:
            return HttpResponse("The type of operation is not specified or incorrect.", status=400)

        filters = {"user": request.user}
        if card_id:
            filters["card__id"] = card_id
        if month:
            filters["date__month"] = int(month)
        if year:
            filters["date__year"] = int(year)

        queryset = Model.objects.filter(**filters)

        if not queryset.exists():
            return HttpResponse("Нет данных для экспорта", status=404)

        data = []
        for obj in queryset:
            data.append(
                {
                    "category": obj.category.get_name(request.user.language),
                    "amount": float(obj.amount),
                    "description": obj.description,
                    "date": obj.date.strftime("%Y-%m-%d"),
                }
            )

        df = pd.DataFrame(data)

        if export_format == "xlsx":
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            filename = f"{operation_type}_data_{datetime.now().date()}.xlsx"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

            with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)

            return response

        response = HttpResponse(content_type="application/json")
        filename = f"{operation_type}_data_{datetime.now().date()}.json"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.write(df.to_json(orient="records", force_ascii=False, indent=2))

        return response
