from rest_framework import serializers

from ..models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "status", "views"]
        read_only_fields = []
        depth = 1
