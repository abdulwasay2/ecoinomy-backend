from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import get_adapter
from user.models import Profile
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

from django.core.mail import send_mail
from django.template.loader import render_to_string


class AccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        try:
            send_mail(
                template_prefix,
                email,
                context,
                subject="Please Verify Your Account",
            )
        except Exception as e:
            print("Context: ", context)
            print("Error: ", e)
            print("Error sending confirmation email.")

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        profile = Profile()
        validated_data = form.data
        if validated_data:
            for data in validated_data:
                setattr(profile, data, validated_data[data])
        user.email = profile.email
        profile.user_id = user.id
        profile.save()
        return user