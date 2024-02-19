from rest_framework import serializers
from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id','name','status','file','slug','created','updated',]
        read_only_fields = ['owner',]
        depth = 1

    def create(self, validated_data):
        return super().create(validated_data)
