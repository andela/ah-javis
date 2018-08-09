import re
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator

from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article, Rate


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model format to Json format
    """
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    slug = serializers.SlugField(required=False)
    image_url = serializers.URLField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    author = ProfileSerializer(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'slug', 'body',
                  'description', 'image_url', 'created_at', 'updated_at',
                  'author', 'likes', 'dislikes',
                  'likes_count', 'dislikes_count']

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def validate(self, data):
        # The `validate` method is used to validate the title,
        # description and body
        title = data.get('title', None)
        description = data.get('description', None)

        return data

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()


class RateSerializer(serializers.Serializer):
    """Serializers registration requests and creates a new rate."""

    rate = serializers.IntegerField(required=True)

    def validate(self, data):
        """Check that rate is valid"""
        rating = data.get('rate')
        if rating == '':
            raise serializers.ValidationError('Rate is required.')
        # Validate the rate is between 0 and 5.
        if rating < 0 or rating > 5:
            raise serializers.ValidationError(
                'Rate should be from 0 to 5.')

        return {"rate": rating}
