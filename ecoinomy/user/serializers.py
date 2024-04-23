from rest_framework import serializers
from user.models import User, Profile
from django_countries.serializer_fields import CountryField


class ProfileSerializer(serializers.ModelSerializer):
    country = CountryField(required=False)
    class Meta:
        model = Profile
        # fields = "__all__"
        exclude = ['user']

class UserSerializer(serializers.Serializer):
    profile = ProfileSerializer(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, *args, **kwargs):
        profile_data = self.validated_data.get("profile", None)
        if profile_data:
            email = profile_data.get("email")
            phone_number = profile_data.get("phone_number")
            user_data = {}

            if email is None and phone_number is None:
                raise serializers.ValidationError({"error": "email or phone_number. atleast one field is required"})
            
            if phone_number:
                profile = Profile.objects.filter(phone_number=phone_number)
                if profile:
                    return profile
            
            if email:
                profile = Profile.objects.filter(email=email)
                if profile:
                    return profile

                user_data["email"] = email

            profile_data["email"] = email
            profile_data["phone_number"] = phone_number
            user = User.objects.create(**user_data)
            Profile.objects.create(user=user, **profile_data)
            return {"message": "Otp send to user email or phone number"}
        else:
            raise serializers.ValidationError({"error": "email or phone_number. atleast one field is required"})


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return super().update(instance, validated_data)
    

class UserPasswordChangeSerializer(serializers.Serializer):

    new_password = serializers.CharField()
    old_password = serializers.CharField()