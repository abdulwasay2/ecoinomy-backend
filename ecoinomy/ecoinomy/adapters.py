from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import get_adapter
from user.models import Profile
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

from django.core.mail import send_mail
from django.template.loader import render_to_string


class AccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        email = emailconfirmation.email_address.email
        # activate_url = f"example.com/{emailconfirmation.key}"
        ctx = {"code": emailconfirmation.key, "domain": ""}
        email_template = "email/code_send.html"
        self.send_mail(email_template, email, ctx)

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


    def save_user(self, request, user, validated_data, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        # password = AbstractBaseUser.set_unusable_password(self)
        # user.set_password(password)
        
        profile = Profile()
        # if validated_data:
        #     for data in validated_data:
        #         setattr(profile, data, validated_data[data])
        user.email = profile.email
        print("user.id:", user)
        print("profile:", profile.id)
        profile.user_id = user.id
        # user.profile = profile
        if commit:
            user.save()
        profile.save()
        return user
