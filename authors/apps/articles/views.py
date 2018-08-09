from django.shortcuts import render
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from .renderers import ArticleJSONRenderer, FavoriteJSONRenderer
from .models import Article


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
        serializer_context = {'request': request}
        article = request.data.get('article', {})
        serializer = self.serializer_class(
            data=article, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user.profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        '''
        Get all articles
        '''
        serializer_context = {'request': request}
        queryset = Article.objects.all()
        serializer = self.serializer_class(
            queryset, many=True,
            context=serializer_context)

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

        if not serializer_instance.author.id == request.user.profile.id:
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
        serializer.save()

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


class FavoriteAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (FavoriteJSONRenderer,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self, request, slug):
        """
        Override the retrieve method to get a article
        """
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug doesn't exist")

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        """
        Method that favorites articles.
        """
        serializer_context = {'request': request}
        try:
            article = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")

        request.user.profile.favorite(article)

        serializer = self.serializer_class(
            article,
            context=serializer_context
        )
        return Response(serializer.data,  status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        """
        Method that favorites articles.
        """
        serializer_context = {'request': request}
        try:
            article = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist")

        request.user.profile.unfavorite(article)

        serializer = self.serializer_class(
            article,
            context=serializer_context
        )
        return Response(serializer.data,  status=status.HTTP_200_OK)
