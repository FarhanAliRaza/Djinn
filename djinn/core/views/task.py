from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from ..models import Task
from ..serializers.task import TaskSerializer


class TaskView(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):

        if self.request.user != instance.owner:
            raise ValidationError("You do not have permission to delete this task", code=status.HTTP_403_FORBIDDEN)

        instance.delete()
        