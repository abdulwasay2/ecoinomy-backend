from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from django_countries import countries

from article.serializers import ArticleSerializer, ArticleAuthorSerializer, ArticleViewsSerializer, SnippetSerializer
from article.models import Article, ArticleType, ArticleViews, ArticleAuthor, Snippet
from article.filters import ArticleFilter
from ecoinomy.views import DefaultOrderingMixin


class ArticleViewSet(DefaultOrderingMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = ArticleFilter
    ordering_fields = ['heading', 'created_at']
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
    
    @action(methods=["GET"], detail=False)
    def get_article_types(self, request, *args, **kwargs):
        return Response(data={"types": ArticleType.choices})
    
    @action(methods=["GET"], detail=False)
    def get_countries(self, request, *args, **kwargs):
        return Response(data={"countries": list(countries)})


class ArticleAuthorViewSet(DefaultOrderingMixin, ModelViewSet):
    serializer_class = ArticleAuthorSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = ArticleAuthor.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class ArticleViewsViewSet(DefaultOrderingMixin, ModelViewSet):
    serializer_class = ArticleViewsSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = ArticleViews.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return (permissions.IsAuthenticated,)
        return super().get_permissions()


class SnippetViewSet(DefaultOrderingMixin, ModelViewSet):
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Snippet.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
