from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response


try:
    from allauth.utils import email_address_exists
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


# Create your views here.
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        if user.email and email_address_exists(user.email):
            ...
            # raise validation here
            # response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

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
