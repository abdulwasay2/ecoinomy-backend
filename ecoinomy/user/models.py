from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from ecoinomy.models import BaseModel
from django.db.models import Q, CheckConstraint



default_settings = dict(
    add_similar_products_across_stores=True
)

class Gender(models.Choices):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    PREFER_NOT_TO_SAY = 'prefer_not_to_say'


# Create your models here.
class Profile(BaseModel):
    class Meta:
        db_table = "profile"

    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField("Email address", unique=True, max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    country = CountryField(max_length=255, null=True, blank=True, default="Australia")
    nationality = CountryField(max_length=255, null=True, blank=True, default="Australia")
    city = models.CharField(max_length=255, null=True, blank=True, default="")
    address = models.CharField(max_length=255, null=True, blank=True, default="")
    postcode = models.CharField(max_length=15, verbose_name="Postcode/ Zipcode", null=True, blank=True, default="")
    date_of_birth = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=255, choices=Gender.choices, null=True, blank=True)
    display_picture = models.FileField(upload_to="profile_media", blank=True, null=True)
    prefrences = models.JSONField(default=default_settings)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(email__isnull=False) | Q(phone_number__isnull=False),
                name='Either a phone number or an email is required. At least one must be provided'
            )
        ]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        profile_fields = {
            "first_name": extra_fields.pop("first_name", ""),
            "phone_number": extra_fields.pop("phone_number", ""),
        }
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_unusable_password()
        if password:
            user.set_password(password)
        profile = Profile(email=email)
        profile.user = user
        profile.update(profile_fields)
        user.save(using=self._db)
        profile.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField("Email address", unique=True, null=True, blank=True)
    # location = models.PointField(geography=True, blank=True, null=True)

    # Permissions
    is_active = models.BooleanField("Is active", default=True)
    is_superuser = models.BooleanField("Is admin", default=False)
    has_completed_registration = models.BooleanField(default=False)

    # Meta
    date_joined = models.DateTimeField("Date joined", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"

    def __str__(self):
        return str(self.id)

    @property
    def is_staff(self):
        return True
