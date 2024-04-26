from rest_framework import serializers
from category.models import Category, CarousalItem


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CarouselSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarousalItem
        fields = '__all__'
