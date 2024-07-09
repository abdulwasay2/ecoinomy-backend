from rest_framework import serializers
from user.models import User, Profile
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumber
from drf_extra_fields.fields import Base64ImageField

from eco_auth.serializers import UserGroupSerializer


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # country = CountryField(required=False)
    # nationality = CountryField(required=False)
    # phone_number = PhoneNumber()
    display_picture = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ("id", "user", "created_at", "updated_at")


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    email = serializers.EmailField(required=False)
    groups = UserGroupSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ["profile", "email", "username", "groups"]

    # def create(self, *args, **kwargs):
    #     profile_data = self.validated_data.get("profile", None)
    #     if profile_data:
    #         email = profile_data.get("email")
    #         phone_number = profile_data.get("phone_number")
    #         user_data = {}

    #         if email is None and phone_number is None:
    #             raise serializers.ValidationError({"error": "email or phone_number. atleast one field is required"})
            
    #         if phone_number:
    #             profile = Profile.objects.filter(phone_number=phone_number)
    #             if profile:
    #                 return profile
            
    #         if email:
    #             profile = Profile.objects.filter(email=email)
    #             if profile:
    #                 return profile

    #             user_data["email"] = email

    #         profile_data["email"] = email
    #         profile_data["phone_number"] = phone_number
    #         user = User.objects.create(**user_data)
    #         Profile.objects.create(user=user, **profile_data)
    #         return {"message": "Otp send to user email or phone number"}
    #     else:
    #         raise serializers.ValidationError({"error": "email or phone_number. atleast one field is required"})
    

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {
        #     "email": {"required": True},
        #     "password": {"required": True}
        # }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        profile = Profile.objects.create(
            user=user,
            email=user.email
            )
        if profile_data:
            profile.update(profile_data)
            profile.save()
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password", None)
        profile = instance.profile
        if profile_data:
            profile.update(profile_data)
            profile.save()
        return super().update(instance, validated_data)


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = '__all__'


class UserPasswordChangeSerializer(serializers.Serializer):

    new_password = serializers.CharField()
    old_password = serializers.CharField()