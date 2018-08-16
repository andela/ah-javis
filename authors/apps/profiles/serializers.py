from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    get_notifications = serializers.BooleanField(source='user.get_notifications')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image','get_notifications',)
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'

