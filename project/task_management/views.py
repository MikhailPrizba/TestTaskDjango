from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateByCustomerSerializer,
    TaskCreateByEmployeeSerializer,
    TaskTakeSerializer,
    TaskCloseSerializer,
)
from .filters import TaskFilter
from .mixins.views import CreateModelMixin
from .permissions import (
    IsTaskCustomerOrEmployee,
    IsTaskEmployee,
    IsEmployee,
    IsCustomer,
)
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TaskRetrieveUpdateViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    """
    ViewSet для получения, обновления и списка задач.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskCustomerOrEmployee]
    filter_backends = [TaskFilter]


class TaskCreateByEmployeeViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
):
    """
    ViewSet для создания задач сотрудниками.
    """

    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsEmployee]
    serializer_class = TaskCreateByEmployeeSerializer

    @swagger_auto_schema(
        responses={
            201: TaskSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TaskCreateByCustomerViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
):
    """
    ViewSet для создания задач клиентами.
    """

    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    serializer_class = TaskCreateByCustomerSerializer

    @swagger_auto_schema(
        responses={
            201: TaskSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TaskEmployeeActionsViewSet(viewsets.GenericViewSet):
    """
    ViewSet для выполнения действий сотрудниками над задачами.
    """

    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTaskEmployee]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.
        """
        if self.action == "take_task":
            return TaskTakeSerializer
        return TaskCloseSerializer

    def _update_task(self, request, task, data, serializer_class):
        """
        Обновляет задачу с использованием указанного сериализатора.
        """
        serializer = serializer_class(
            task, data=data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        full_serializer = TaskSerializer(task, context={"request": request})
        return Response(full_serializer.data)

    @swagger_auto_schema(
        method="post",
        responses={
            200: TaskSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated, IsEmployee],
    )
    def take_task(self, request, pk=None):
        """
        Действие для взятия задачи сотрудником.
        """
        task = self.get_object()
        return self._update_task(
            request, task, data={}, serializer_class=self.get_serializer_class()
        )

    @swagger_auto_schema(
        method="post",
        responses={
            200: TaskSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    @action(
        detail=True,
        methods=["post"],
    )
    def close_task(self, request, pk=None):
        """
        Действие для закрытия задачи сотрудником.
        """
        task = self.get_object()
        return self._update_task(
            request,
            task,
            data=request.data,
            serializer_class=self.get_serializer_class(),
        )
