from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from category.serializers import (
    CategorySerializers,
)

from .models import Cateogry


class CategoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Viewset for performing crud operations on the 
    logged in user entity \n
    :route params \n
           : id is the id of the existing user object 
    """
    serializer_class = CategorySerializers
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=1)
    
    def get_queryset(self):
        return Cateogry.objects.filter(id=1)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
