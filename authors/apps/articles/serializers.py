import re
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import default_token_generator

from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article, Rate


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

#    class Meta:
 #       model = Rate
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
  #      fields = ['rate', 'counter', 'article', 'rate']

   # def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
    #    return Rate.objects.create(**validated_data)
