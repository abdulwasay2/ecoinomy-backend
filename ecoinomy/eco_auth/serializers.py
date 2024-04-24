from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


try:
    from allauth.account import app_settings as allauth_settings
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class CustomRegisterSerializers(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    password1 = None
    password2 = None

    # class Meta:
    #     fields = ['email', 'phone_number']

    def validate(self, data):
        return data

    def validate_password1(self, password):
        pass

    def validate_email(self, email):
        return email
