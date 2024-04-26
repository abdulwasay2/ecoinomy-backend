from rest_framework import serializers
from article.models import *


class ArticleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAuthor
        fields = "__all__"


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAuthor
        fields = "__all__"


class ArticleViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleViews
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    article_by = ArticleAuthorSerializer(required=False)

    @staticmethod
    def get_views_count(instance):
        return instance.views.count()

    class Meta:
        model = Article
        fields = ["media", "heading", "body", "body_in_second_language", "sub_category", "article_by",
                  "views_count", "estimated_time_to_read", "article_type", "country"]