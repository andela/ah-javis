from django.shortcuts import render
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Article
from .renders import ArticleJSONRenderer
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .renders import ArticleJSONRenderer
from .models import Article

# Create your views here.


class LikesAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = ArticleSerializer

    def put(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")

        if serializer_instance in Article.objects.filter(dislikes=request.user):
            serializer_instance.dislikes.remove(request.user)

        serializer_instance.likes.add(request.user)

        serializer = self.serializer_class(
            serializer_instance, context=serializer_context, partial=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DislikesAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = ArticleSerializer

    def put(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")

        if serializer_instance in Article.objects.filter(likes=request.user):
            serializer_instance.likes.remove(request.user)

        serializer_instance.dislikes.add(request.user)

        serializer = self.serializer_class(
            serializer_instance,  context=serializer_context, partial=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleAPIView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    This class defines the create behavior of our articles.
    '''
    lookup_field = 'slug'
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer, )

    def create(self, request):
        '''
        Create an article
        '''
        article = request.data.get('article', {})
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user.profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        '''
        Get all articles
        '''
        queryset = Article.objects.all()
        serializer = self.serializer_class(
            queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        '''
        Get one article
        '''
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('Article not found')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context

        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        '''
        Edit an article
        '''
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('Artiicle not found')

        if not serializer_instance.author_id == request.user.profile.id:
            raise PermissionDenied(
                'You do not have permission to edit this article')

        serializer_data = request.data.get('article', )

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, slug):
        '''
        Delete an article
        '''
        try:
            article = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('Article not found')

        if article.author_id == request.user.profile.id:
            article.delete()
        else:
            raise PermissionDenied(
                'You do not have permission to delete this article')

        return Response(None, status=status.HTTP_204_NO_CONTENT)
