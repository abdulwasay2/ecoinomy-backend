from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from article import views


router = DefaultRouter()

router.register(r"", views.ArticleViewSet, basename='article-views')
router.register(r"article_author", views.ArticleAuthorViewSet, basename="article_author")
router.register(r"article_views", views.ArticleViewsViewSet, basename="article_author")
router.register(r"snippet", views.SnippetViewSet, basename="article_author")


urlpatterns = [
    re_path("", include(router.urls)),
]