from rest_framework import serializers

from notifications.models import Notification
from authors.apps.articles.models import Article, Comment, User
from authors.apps.articles.serializers import ArticleSerializer
from authors.apps.articles.serializers import CommentSerializer
from authors.apps.authentication.serializers import UserSerializer




class GenericNotificationRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Article):
            serializer = ArticleSerializer(value)
        if isinstance(value, Comment):
           serializer = CommentSerializer(value)
        if isinstance(value, User):
            serializer = UserSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    actor = GenericNotificationRelatedField(read_only=True) 
    class Meta:
        model = Notification

        fields = ('actor',)
