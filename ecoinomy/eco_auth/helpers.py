from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.http import base36_to_int, int_to_base36
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare, salted_hmac
from pyotp import TOTP
from django.core.mail import send_mail

from ecoinomy.utils import send_text_message_text_magic


class UserTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator:
        - user pk in token
        - expires after 15 minutes
        - longer hash (40 instead of 20)
    """

    KEY_SALT = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    SECRET = settings.SECRET_KEY
    EXPIRY_TIME = 60 * 15

    def make_token(self, user):
        return self._make_token_with_timestamp(user, int(timezone.datetime.now().timestamp()))

    def check_token(self, user=None, token=None):
        user_model = get_user_model()
        if not token:
            return None
        try:
            token = str(token)
            user_pk, ts_b36, token_hash = token.rsplit("-", 2)
            ts = base36_to_int(ts_b36)
            user = user_model._default_manager.get(pk=user_pk)
        except (ValueError, TypeError, user_model.DoesNotExist):
            return None

        if (timezone.datetime.now().timestamp() - ts) > self.EXPIRY_TIME:
            return None  # pragma: no cover

        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return None  # pragma: no cover

        return user

    def _make_token_with_timestamp(self, user, timestamp: int, **kwargs) -> str:
        ts_b36 = int_to_base36(timestamp)
        token_hash = salted_hmac(
            self.KEY_SALT,
            self._make_hash_value(user, timestamp),
            secret=self.SECRET,
        ).hexdigest()
        return f"{user.pk}-{ts_b36}-{token_hash}"


def phone_number_exists(phone_number):
    users = get_user_model().objects
    ret = users.filter(**{"phone_number" + "__iexact": phone_number}).exists()
    return ret


def get_user_by_email_phone_number(email=None, phone_number=None):
    users = get_user_model().objects
    ret = None
    if email and phone_number:
        ret = users.filter(Q(profile__phone_number__iexact=phone_number) | Q(email__iexact=email)).first()
    elif email:
        ret = users.filter(email__iexact=email).first()
    elif phone_number:
        ret = users.filter(profile__phone_number__iexact=phone_number).first()
    return ret


def generate_otp(secret=settings.OTP_SECRET_KEY, interval=300):
    return TOTP(secret, interval=interval)


def send_login_otp_to_user(email=None, phone_number=None):
    subject = "Ecoinomy Login OTP"
    code = generate_otp().now()
    message = f"Your one time passcode for login is {code}"
    print(message) 
    if email:
        send_mail(
            subject,
            message,
            settings.FROM_EMAIL,
            [email]
        )

    if phone_number:
        send_text_message_text_magic(subject + "\n" + message, [phone_number])


user_token_generator = UserTokenGenerator()