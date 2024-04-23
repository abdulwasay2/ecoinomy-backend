from django.utils.translation import gettext_lazy as _
from requests.exceptions import HTTPError
from rest_framework import serializers
from rest_framework.reverse import reverse


try:
    from allauth.account import app_settings as allauth_settings
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class CustomRegisterSerializers(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    phone_number = serializers.CharField(required=False)
    password1 = None
    password2 = None

    def validate(self, data):
        pass

    def validate_password1(self, password):
        pass

    def validate_email(self, email):
        return email
