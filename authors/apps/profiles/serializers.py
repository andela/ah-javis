from rest_framework import serializers
from notifications.models import Notification
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ArticleSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image',)
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'


class GenericNotificationRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Article):
            serializer = (ArticleSerializer)

        return serializer.data


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    target = GenericNotificationRelatedField(read_only=True)

    class Meta:
        model = Notification

        fields = ('actor', 'target')
