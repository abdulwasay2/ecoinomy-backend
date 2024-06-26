from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from user.serializers import (
    UserListSerializer,
    UserSerializer, 
    ProfileSerializer,
    User,
    Profile,
    UserPasswordChangeSerializer
)
from user import helpers as user_helper
from user.filters import UserFilter
from ecoinomy.views import DefaultOrderingMixin


class UserViewSet(DefaultOrderingMixin, viewsets.ModelViewSet):
    """
    Viewset for performing crud operations on the 
    logged in user entity \n
    :route params \n
           : id is the id of the existing user object 
    """
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = UserFilter
    ordering_fields = ['email', 'created_at']
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ["change_password"]:
            return UserPasswordChangeSerializer
        if self.action in ["list"]:
            return UserListSerializer
        return super().get_serializer_class()

    @action(methods=["POST"], detail=False)
    def change_password(self, request):
        serialized = self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        current_user = request.user
        if current_user.check_password(serialized.validated_data.get("old_password")):
            current_user.set_password(serialized.validated_data.get("new_password"))
            current_user.save()
            return Response({"detail": "password changed successfully."})
        else:
            raise ValidationError(detail="The old password doesn't match")


class ProfileViewSet(DefaultOrderingMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for performing crud operations on the 
    logged in User Profile entity \n
    :route params \n
           : parent_lookup_user_id is the logged in user's id \n
           : id is the id of the existing user object 
    """

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        current_user = self.request.user
        return Profile.objects.filter(user=current_user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
