import json
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from django_countries import countries

from article.serializers import ArticleSerializer, ArticleAuthorSerializer, ArticleViewsSerializer, SnippetSerializer
from article.models import Article, ArticleType, ArticleViews, ArticleAuthor, Snippet
from article.filters import ArticleFilter, SnippetFilter
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
    
    def create(self, request, *args, **kwargs):
        if "multipart/form-data" in request.headers.get("Content-Type"):
            article_by = json.loads(request.data.pop("article_by", ['{}'])[0])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if "multipart/form-data" in request.headers.get("Content-Type"):
            serializer.validated_data.update({"article_by": article_by})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
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
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = SnippetFilter
    ordering_fields = ['heading', 'created_at']
    queryset = Snippet.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
