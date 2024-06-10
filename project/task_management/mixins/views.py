from rest_framework.response import Response
from rest_framework import status, viewsets
from task_management.serializers import (
    TaskSerializer,
)


class CreateModelMixin(viewsets.mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        full_serializer = TaskSerializer(task)

        headers = self.get_success_headers(full_serializer.data)
        return Response(
            full_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
