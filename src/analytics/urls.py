from django.urls import path

from analytics.bar_chart.views import BarChartDataAPIView
from analytics.export.views import ExportOperationsAPIView
from analytics.pie_chart.views import PieChartDataAPIView

urlpatterns = [
    path("pie/", PieChartDataAPIView.as_view(), name="pie-chart"),
    path("bar/", BarChartDataAPIView.as_view(), name="bar-chart"),
    path("export/", ExportOperationsAPIView.as_view(), name="export-operations"),
]
