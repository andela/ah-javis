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
        ratings = request.data.get("rate", {})
        try:
            article = Article.objects.filter(slug=slug).first()

        except Article.DoesNotExist:
            return Response({"errors":{"message":["Article doesnt exist."]}})

        serializer = self.serializer_class(data=ratings)
        serializer.is_valid(raise_exception=True)
        rate = serializer.data.get('rate')
        rating = Rate.objects.filter(article=article,
                rater=request.user.profile).first()
        
        if not rating:
            rating = Rate(article=article, rater=request.user.profile, ratings=rate)
            rating.save()
            avg_ratings = Rate.objects.filter(article=article).aggregate(Avg('ratings'))
            return Response({"response":{"message":["Successfull."],
                "avg_ratings":avg_ratings
                }}, status=status.HTTP_201_CREATED)

        if rating.counter > 3: 
            return Response({"errors":{"message":["You are only allowed to"
            "rate 3 times"]}}, status=status.HTTP_403_FORBIDDEN)

        rating.ratings = rate
        rating.save()
        avg = Rate.objects.filter(article=article).aggregate(Avg('ratings'))
        return Response({"avg":avg}, status=status.HTTP_201_CREATED)
