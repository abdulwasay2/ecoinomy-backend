from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Count, Prefetch, Subquery

from category.serializers import (
    CategorySerializer,
    CarouselSerializer,
    SuggestedCategorySerializer
)
from category.models import Category, CarousalItem
from article.models import Article
from category.filters import CategoryFilter
from ecoinomy.views import DefaultOrderingMixin


class CategoryViewSet(DefaultOrderingMixin, viewsets.ModelViewSet):
    """"""

    serializer_class = CategorySerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = CategoryFilter
    ordering_fields = ['name', 'created_at']
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ["get_suggested_categories"]:
            return SuggestedCategorySerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "get_suggested_categories"]:
            return [AllowAny()]
        return super().get_permissions()
    
    @action(methods=["GET"], detail=False)
    def get_suggested_categories(self, request, *args, **kwargs):
        articles_sub_q = Subquery(
            Article.objects.annotate(count=Count("views")).values_list(
                "id", flat=True).order_by("-count")[:1])
        categories = Category.objects.annotate(
        view_count=Count("articles__views")).prefetch_related(
            Prefetch(
                "articles",
                queryset=Article.objects.filter(id__in=articles_sub_q),
            )
        ).order_by("-view_count")[:5]
        serializer = self.get_serializer(categories, many=True)
        return Response(data={"data": serializer.data})


class CarouselViewSet(DefaultOrderingMixin, viewsets.ModelViewSet):
    """"""

    serializer_class = CarouselSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = CarousalItem.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()
