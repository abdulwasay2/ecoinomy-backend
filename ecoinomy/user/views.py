from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from user.serializers import (
    UserSerializer, 
    ProfileSerializer,
    User,
    Profile
)
from user import helpers as user_helper


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Viewset for performing crud operations on the 
    logged in user entity \n
    :route params \n
           : id is the id of the existing user object 
    """
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(self.get_queryset())
    
    def get_queryset(self):
        return Profile.objects.filter(user_id=1)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class ProfileViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Viewset for performing crud operations on the 
    logged in User Profile entity \n
    :route params \n
           : parent_lookup_user_id is the logged in user's id \n
           : id is the id of the existing user object 
    """

    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(self.get_queryset())
    
    def get_queryset(self):
        return Profile.objects.filter(user_id=1)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
