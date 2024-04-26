from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from category.serializers import (
    CategorySerializers,
    CarouselSerializers
)
from category.models import Category, CarousalItem


class CategoryViewSet(viewsets.ModelViewSet):
    """"""

    serializer_class = CategorySerializers
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (AllowAny,)
        return super().get_permissions()


class CarouselViewSet(viewsets.ModelViewSet):
    """"""

    serializer_class = CarouselSerializers
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = CarousalItem.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (AllowAny,)
        return super().get_permissions()
