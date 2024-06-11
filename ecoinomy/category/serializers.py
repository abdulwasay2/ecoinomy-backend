from rest_framework import serializers
from category.models import Category, CarousalItem
from article.serializers import ArticleSerializer


class SubCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryNameSerializer(required=False, many=True)
    
    class Meta:
        model = Category
        fields = '__all__'


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarousalItem
        fields = '__all__'


class SuggestedCategorySerializer(CategorySerializer):
    articles = ArticleSerializer(many=True, required=False)