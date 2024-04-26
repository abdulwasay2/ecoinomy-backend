from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.encoding import force_str
from phonenumber_field.serializerfields import PhoneNumber
from dj_rest_auth.serializers import (
    PasswordResetSerializer as BasePasswordResetSerializer,
    PasswordResetConfirmSerializer as BasePasswordResetConfirmSerializer,
    UserModel,
)
from django.conf import settings

from eco_auth.helpers import generate_otp
from eco_auth.forms import PasswordResetForm


try:
    from allauth.account import app_settings as allauth_settings
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class CustomRegisterSerializers(RegisterSerializer):
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumber()
    password1 = None
    password2 = None

    def validate(self, data):
        if "email" not in data and "phone_number" not in data:
            raise serializers.ValidationError(detail="Please provide either phone number or email for login")
        return data

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        return email

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
    

class OTPVerifySerializer(serializers.Serializer):

    ephemeral_token = serializers.CharField()
    code = serializers.CharField()


class PasswordResetSerializer(BasePasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {"template_prefix": "email/password_reset"}
    

class CustomPasswordResetConfirmSerializer(BasePasswordResetConfirmSerializer):
    uid = None
    token = None
    key = serializers.CharField(required=True)

    def validate(self, attrs):
        from django.utils.http import urlsafe_base64_decode as uid_decoder

        # Decode the uidb64 (allauth use base36) to uid to get User object
        parsed_key = attrs["key"].split("-")
        try:
            uid = force_str(uid_decoder(parsed_key[-1] if parsed_key else ''))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise serializers.ValidationError({"uid": ["Invalid value"]})

        totp = generate_otp(settings.PASSWORD_RESET_OTP_SECRET)
        if not totp.verify(parsed_key[0] if parsed_key else ''):
            raise serializers.ValidationError({"token": ["Invalid value"]})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs