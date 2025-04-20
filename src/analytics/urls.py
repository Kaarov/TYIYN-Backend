from django.urls import path

from analytics.pie_chart.views import PieChartDataAPIView

urlpatterns = [
    path("pie/", PieChartDataAPIView.as_view(), name="pie-chart"),
]
