from rest_framework import serializers
from .models import Cateogry


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Cateogry
        fields = '__all__'

