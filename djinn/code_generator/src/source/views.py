from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from ..models import Model
from ..serializers.model import ModelSerializer


class ModelViewClass(ModelViewSet):
    serializer_class = ModelSerializer
    filter_backends = [
        DjangoFilterBackend
    ]  # http://example.com/api/products?category=clothing&in_stock=True

    def get_queryset(self):
        """
        This should return queryset from which other operations can happen
        """
        return Model.objects.all()

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
