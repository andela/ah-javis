from django.shortcuts import render

from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RateSerializer
from .renderers import RateJSONRenderer
from .models import Article, Rate
from django.db.models import Avg

class RateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RateSerializer
    renderer_classes = (RateJSONRenderer,)

    def create(self, request, slug):
        """ Rating view"""
        ratings = request.data.get("rate", {})
        # Filter articles with the given slug
        try:
            article = Article.objects.filter(slug=slug).first()

        except Article.DoesNotExist:
            return Response({"errors":{"message":["Article doesnt exist."]}})

       # Check if article is none
        if article is None:
            return Response({"errors":{"message":["Article doesnt exist."]}},
                    404)

        # Serialize rate model
        serializer = self.serializer_class(data=ratings)
        # Check for validation errors
        serializer.is_valid(raise_exception=True)
        rate = serializer.data.get('rate')
        # Filter rate table to check if record with given article and user
        # exist.
        rating = Rate.objects.filter(article=article,
                rater=request.user.profile).first()

        if not rating:
            """ If it doesnt exist create an new record."""
            rating = Rate(article=article, rater=request.user.profile, ratings=rate)
            rating.save()
            # get the averages ratings of the article.
            avg_ratings = Rate.objects.filter(article=article).aggregate(Avg('ratings'))
            return Response({"response":{"message":["Successfull."],
                "avg_ratings":avg_ratings
                }}, status=status.HTTP_201_CREATED)

        # If exist check if the user has exceed rating counter
        if rating.counter > 3: 
            """Allow rating if counter is less than 3."""
            return Response({"errors":{"message":["You are only allowed to"
            "rate 3 times"]}}, status=status.HTTP_403_FORBIDDEN)

        rating.ratings = rate
        rating.save()
        # Get the average ratings of the article.
        avg = Rate.objects.filter(article=article).aggregate(Avg('ratings'))
        return Response({"avg":avg}, status=status.HTTP_201_CREATED)
