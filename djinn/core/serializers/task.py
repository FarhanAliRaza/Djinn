from rest_framework import serializers
from ..models import Task


class TaskSerializer(serializers.ModelSerializer):

    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "status",
            "file",
            "slug",
            "created",
            "updated",
            "owner_id",
        ]
        # fields = "__all__"
        read_only_fields = ["owner", "owner_id"]
        depth = 1

    def create(self, validated_data):
        user = None
        return super().create(validated_data)

    def get_owner_id(self, instance):
        return instance.id


# /home/dev/djinn/djinn/core/serializers/task.py
# /home/dev/djinn/core/serializers/task.py
