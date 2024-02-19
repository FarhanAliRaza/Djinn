from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError
from ..models import Task
from ..serializers.task import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        # do create validation other than serializer validation
        serializer.save()

    def perform_update(self, serializer):
        # perform update validation
        serializer.save()

    def perform_destroy(self, instance):
        # perform validation before deleting instance like if it user owns this instance
        instance.delete()
