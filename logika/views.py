from django.db import connection
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import permissions

from rest_framework.pagination import PageNumberPagination

from . import serializers
from .models import Article, Comment, Category
from .permissions import IsOwnerOrReadOnly



class StandardResultSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.select_related('owner', 'category')
    serializer_class = serializers.ArticleSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('title', 'category')
    pagination_class = StandardResultSetPagination

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print(f'Queries Counted: {len(connection.queries)}')
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(id__icontains=search))
        return queryset


class ArticleCreateView(generics.CreateAPIView):
    serializer_class = serializers.ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class RatingDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.RatingDetailSerializer