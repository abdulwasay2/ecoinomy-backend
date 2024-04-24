from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from allauth.utils import email_address_exists
from dj_rest_auth.utils import jwt_encode
from eco_auth.helpers import phone_number_exists, get_user_by_email_phone_number, \
    user_token_generator
from .serializers import CustomRegisterSerializers


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializers

    def get_response_data(self, user):
        incoming_data = self.request.data
        token = user_token_generator(user)
        medium =  "email" if incoming_data.get("email") else ""
        if not medium:
            medium = "phone number" if incoming_data.get("phone_number") else ""
        return {
            "ephemeral_token": token,
            "message": f"opt sent to your {medium}"
        }

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        import pdb; pdb.set_trace()
        if email_address_exists(data.get("email")):
            user = get_user_by_email_phone_number(**serializer.data)
        else:
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
    
    # def perform_create(self, serializer):
    #     user = serializer.save(self.request)
    #     self.access_token, self.refresh_token = jwt_encode(user)
    #     return user 
