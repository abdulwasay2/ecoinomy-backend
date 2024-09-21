from django.contrib.auth.forms import (
    PasswordResetForm as BasePasswordResetForm,
    UserModel,
)
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# from django.template.loader import render_to_string
from django.core.mail import send_mail

from eco_auth.helpers import generate_otp


class PasswordResetForm(BasePasswordResetForm):
    def save(
        self,
        domain_override=None,
        template_prefix="email/password_reset",
        email_template_name="email/password_reset.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            totp = generate_otp(f"{settings.PASSWORD_RESET_OTP_SECRET}_{user.pk}")
            token = totp.now()
            user_email = getattr(user, email_field_name)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            code = f"{token}-{uid}"
            context = {
                "code": code,
                **(extra_email_context or {}),
            }
            self.send_mail(
                template_prefix,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

    def send_mail(
        self,
        template_prefix,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        to = to_email if isinstance(to_email, list) else [to_email]
        template_prefix = template_prefix
        # message = render_to_string(email_template_name, context).strip()
        # message = f"Hello you can reset the password by clicking this link {context.get('reset_link')}"
        message = f"Hello you can reset the password using this key {context.get('code')}"
        print(message)
        send_mail(
            recipient_list=to,
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=message,
            # html_message=message,
            # template_prefix=template_prefix,
            # context=context,
            subject="Reset Your Password!"
        )
