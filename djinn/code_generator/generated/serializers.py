from rest_framework import serializers
from ..models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "body", "status"]
        read_only_fields = []
        depth = 1
