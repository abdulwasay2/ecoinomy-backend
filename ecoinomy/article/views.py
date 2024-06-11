from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from article.serializers import ArticleSerializer, ArticleAuthorSerializer, ArticleViewsSerializer, SnippetSerializer
from article.models import Article, ArticleViews, ArticleAuthor, Snippet


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = CategoryFilter
    ordering_fields = ['name', 'created_at']
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Article.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_object(self):
        instance = super().get_object()
        if self.action in ['retrieve'] and not self.request.user.is_superuser:
            ArticleViews.objects.get_or_create(
                article_id=instance.id,
                user_id=self.request.user.id
            )
        return instance


class ArticleAuthorViewSet(ModelViewSet):
    serializer_class = ArticleAuthorSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = ArticleAuthor.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class ArticleViewsViewSet(ModelViewSet):
    serializer_class = ArticleViewsSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = ArticleViews.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return (permissions.IsAuthenticated,)
        return super().get_permissions()


class SnippetViewSet(ModelViewSet):
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Snippet.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
