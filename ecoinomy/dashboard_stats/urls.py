from django.urls import path
from dashboard_stats.views import *


urlpatterns = [
    path("general_stats/", DashboardStatsView.as_view(), name="general-stats"),
    path("line_plot_data/", DashboardGraphsDataView.as_view(), name="line-plot-data"),
]
