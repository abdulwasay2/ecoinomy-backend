
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone

from dashboard_stats.helpers import (
    get_total_entity_count, 
    get_per_day_entity_count_between_dates, 
    get_total_entity_count_between_dates
)
from user.models import Profile
from article.models import Article, ArticleViews


class DashboardStatsView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, **kwargs):
        current_date = timezone.now().date() 
        # most_recent_monday = current_date - timezone.timedelta(days=current_date.weekday())
        most_recent_monday = current_date
        start_of_prev_week = most_recent_monday - timezone.timedelta(days=7)
        end_of_prev_week = most_recent_monday - timezone.timedelta(days=1)
        response = {
            "total_users": get_total_entity_count(Profile),
            "total_articles": get_total_entity_count(Article),
            "last_week_joined_users": get_total_entity_count_between_dates(Profile, [start_of_prev_week, end_of_prev_week]),
            "last_week_article_visits": get_total_entity_count_between_dates(ArticleViews, [start_of_prev_week, end_of_prev_week])
        }

        return Response(data=response)
    

class DashboardGraphsDataView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, **kwargs):
        current_date = timezone.now().date() 
        # most_recent_monday = current_date - timezone.timedelta(days=current_date.weekday())
        most_recent_monday = current_date
        start_of_prev_week = most_recent_monday - timezone.timedelta(days=7)
        end_of_prev_week = most_recent_monday - timezone.timedelta(days=1)
        response = {
            "last_week_joined_users_line_data": get_per_day_entity_count_between_dates(
                Profile, [start_of_prev_week, end_of_prev_week]),
            "last_week_article_visits_line_data": get_per_day_entity_count_between_dates(
                ArticleViews, [start_of_prev_week, end_of_prev_week])
        }

        return Response(data=response)