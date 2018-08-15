from rest_framework import serializers

from notifications.models import Notification
from authors.apps.articles.models import Article, Comment, User
from authors.apps.articles.serializers import ArticleSerializer
from authors.apps.articles.serializers import CommentSerializer
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer




class GenericNotificationRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        actor_type =  None
        if isinstance(value, Article):
            actor_type = "article"
            serializers = ArticleSerializer(value)
        if isinstance(value, Comment):
            actor_type = "comment"
            serializer = CommentSerializer(value)
        if isinstance(value, User):
            actor_type = "user"
            serializer = ProfileSerializer(value.profile)

        return {
            "type":actor_type,
            "data":serializer.data 
        }


class NotificationSerializer(serializers.ModelSerializer):
    actor = GenericNotificationRelatedField(read_only=True) 
    class Meta:
        model = Notification

        fields = ('actor','verb','target', 'level', 'unread', 'timestamp', )
