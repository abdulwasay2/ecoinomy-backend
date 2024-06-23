from rest_framework import serializers
from article.models import *
from category.models import Category


class ArticleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAuthor
        fields = "__all__"


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = "__all__"


class ArticleViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleViews
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    article_by = ArticleAuthorSerializer(required=False)
    sub_category_details = serializers.SerializerMethodField(required=False)

    @staticmethod
    def get_views_count(instance):
        return instance.views.count()
    
    @staticmethod
    def get_sub_category_details(instance):
        return Category.objects.filter(id=instance.sub_category_id).values()

    class Meta:
        model = Article
        fields = ["id", "media", "heading", "body", "body_in_second_language", "sub_category", "article_by",
                  "views_count", "estimated_time_to_read", "article_type", "country", "sub_category_details"]
        
    def create(self, validated_data):
        author = validated_data.pop("article_by")
        if author:
            author, _ =ArticleAuthor.objects.get_or_create(**author)
            validated_data.update({"article_by_id": author.id})
        article = super().create(validated_data)
        return article
    
    def update(self, instance, validated_data):
        author = validated_data.pop("article_by")
        if author:
            author, _ =ArticleAuthor.objects.get_or_create(**author)
            validated_data.update({"article_by_id": author.id})
        return super().update(instance, validated_data)