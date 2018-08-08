from rest_framework import serializers

from authors.apps.profiles.serializers import ProfileSerializer

from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        article = self.context['article']
        author = self.context['author']

        return Comment.objects.create(
            author=author, article=article, **validated_data
        )