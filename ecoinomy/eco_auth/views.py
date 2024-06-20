from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status, permissions, viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from allauth.utils import email_address_exists
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.serializers import JWTSerializer

from eco_auth.helpers import phone_number_exists, get_user_by_email_phone_number, \
    user_token_generator, send_login_otp_to_user, generate_otp
from .serializers import CustomRegisterSerializers, OTPVerifySerializer, \
    GroupSerializer, Group, PermissionSerializer, Permission


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializers

    def get_response_data(self, user):
        incoming_data = self.request.data
        token = user_token_generator.make_token(user)
        medium =  "email" if incoming_data.get("email") else ""
        if not medium:
            medium = "phone number" if incoming_data.get("phone_number") else ""
        if medium:
            send_login_otp_to_user(**incoming_data)
        return {
            "ephemeral_token": token,
            "message": f"opt sent to your {medium}"
        }

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_user_by_email_phone_number(**serializer.data)
        if not user:
            user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class VerifyOTPView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OTPVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_token_generator.check_token(token=serializer.validated_data["ephemeral_token"])
        if not user:
            raise ValidationError("ephemeral_token expired or invalid")
        valid_code = generate_otp().verify(serializer.validated_data["code"])
        if not valid_code:
            raise ValidationError("otp code expired or invalid")
        access_token, refresh_token = jwt_encode(user)
        data = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        serializer = JWTSerializer(data, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):

    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Group.objects.all()


class PermissionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    queryset = Permission.objects.all()