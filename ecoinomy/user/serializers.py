from rest_framework import serializers
from user.models import User, Profile
from django_countries.serializer_fields import CountryField


class ProfileSerializer(serializers.ModelSerializer):
    country = CountryField(required=False)
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("id", "username", "is_superuser", "has_completed_registration")
        fields = '__all__'

    def create(self, *args, **kwargs):
        profile_data = self.validated_data.pop('profile')
        user = User.objects.create(**self.validated_data)
        # Profile.objects.create(user=user, **profile_data)
        return user

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