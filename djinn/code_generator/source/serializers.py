from rest_framework import serializers
from ..models import Model


class ModelSerializer(serializers.ModelSerializer):  # Do not change name
    class Meta:
        model = Model
        fields = []
        read_only_fields = []
        depth = 1
