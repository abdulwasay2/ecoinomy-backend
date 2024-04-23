import re

from allauth.account.models import EmailAddress
from django.shortcuts import get_object_or_404
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework.exceptions import ValidationError
# from django.contrib.gis.measure import D
# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.geos import Point
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from user.models import User, Profile


def create_user(request, data):
    """
    creates user using allauth adapter

    :param request: the request object
    :param data: the validated data of the user serializer
    :return the created user object and the new email address
    """
    adapter = get_adapter()
    user = adapter.new_user(request)
    adapter.save_user(request, user, data)
    email_address = setup_user_email(request, user, [])
    return user, email_address


def update_user(instance, validated_data):
    """
    updates the user

    :param instance: the user object to update
    :param validated_data: the validated data from the serializer
    :return: the updated user object
    """
    profile_data = validated_data.pop("profile", {})
    password = validated_data.pop("password", None)
    profile = instance.profile
    profile.picture = validated_data.get("picture", None)
    for data in profile_data:
        if profile_data[data] is not None:
            setattr(profile, data, profile_data[data])
    if password:
        instance.set_password(password)
    for data in validated_data:
        if validated_data[data] is not None:
            setattr(instance, data, validated_data[data])
    profile.save()
    instance.save()
    return instance


def update_profile(instance, validated_data):
    """
    updates the user profile

    :param instance: the profile object to update
    :param validated_data: the validated data from the serializer
    :return: the updated profile object
    """
    instance.user.email = validated_data.get("email", instance.user.email)
    interests = validated_data.pop('interests', None)
    if interests != None or type(interests) == list:
        instance.interests.set(interests)
    for data in validated_data:
        if validated_data[data] is not None:
            setattr(instance, data, validated_data[data])
    instance.user
    instance.save()
    return instance


def get_email_address_by_user(user_id):
    """get email address from db given a user id"""
    return get_object_or_404(EmailAddress, user_id=user_id)


def does_email_exist(email):
    """validates if the user exists in db"""
    return EmailAddress.objects.filter(email=email).filter(verified=True).exists()


def validate_uniqueness(email):
    """validates if the email is correct and exists in db"""
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    is_valid_email = re.search(regex, email)
    if is_valid_email:
        return not does_email_exist(email)
    return False


def resend_user_verification(email, request):
    """
    resend verification email for user
    :param email: email string of the user
    :param request: the request object
    :return:
    """
    # email_address = get_object_or_404(EmailAddress, email=email)
    email_address = EmailAddress.objects.filter(email=email).first()
    if email_address and email_address.verified:
        raise ValidationError("Account already verified")
    if not email_address:
        user = get_object_or_404(User, email=email)
        email_address = EmailAddress.objects.create(email=email, user=user)
    email_address.change(request, email)


def user_display_email(user):
    return getattr(user, "email", user.id)


def change_user_password(user, new_password, old_password):
    if check_password(old_password, user.password):
        # if old_password == new_password:
        #     return 'password already used.'
        user.set_password(new_password)
        user.save()
        return 'password changed successfully'
    return 'old password does not match'