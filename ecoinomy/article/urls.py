from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from article import views


router = DefaultRouter()

router.register(r"article", views.ArticleViewSet, basename='article-views')
router.register(r"article_author", views.ArticleAuthorViewSet, basename="article_author")
router.register(r"article_views", views.ArticleViewsViewSet, basename="article")
router.register(r"snippet", views.SnippetViewSet, basename="snippet")


urlpatterns = [
    re_path("", include(router.urls)),
]