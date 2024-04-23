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


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset for performing crud operations on the 
    logged in user entity \n
    :route params \n
           : id is the id of the existing user object 
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # allow anonymous
    permission_classes = (AllowAny,)

    def get_object(self):
        request = self.request
        current_user = request.user
        return get_object_or_404(self.get_queryset(), id=1)
    
    def get_queryset(self):
        request = self.request
        current_user = request.user
        return User.objects.filter(id=1)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    viewsets.GenericViewSet
):
    """
    Viewset for performing crud operations on the 
    logged in User Profile entity \n
    :route params \n
           : parent_lookup_user_id is the logged in user's id \n
           : id is the id of the existing user object 
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # parser_classes = (MultiPartJSONParser,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        request = self.request
        current_user = request.user
        return get_object_or_404(self.get_queryset(), user_id=current_user.id)

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = user_helper.update_profile(instance, serializer.data)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)