from django.urls import path

from analytics.bar_chart.views import BarChartDataAPIView
from analytics.pie_chart.views import PieChartDataAPIView

urlpatterns = [
    path("pie/", PieChartDataAPIView.as_view(), name="pie-chart"),
    path("bar/", BarChartDataAPIView.as_view(), name="bar-chart"),
]
