from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from ..models import Blog
from ..serializers.blog import BlogSerializer


class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # http://example.com/api/products?category=clothing&in_stock=True

    def get_queryset(self):
        """
        This should return queryset from which other operations can happen
        """
        return Blog.objects.all()

    def perform_create(self, serializer):
        """
        validations before create
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        update validations
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        validations before delete
        """
        instance.delete()
