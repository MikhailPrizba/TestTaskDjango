from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class TaskFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        Фильтрация задач в зависимости от роли пользователя и параметров запроса.
        """
        user = request.user

        # Фильтрация по статусу задачи
        status = request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Фильтрация по пользователю (сотруднику или заказчику)
        if user.user_role == user.UserRoleChoices.CUSTOMER:
            queryset = queryset.filter(customer=user)
        elif user.has_perm("task_management.view_all_tasks"):
            # Сотрудник с правом доступа ко всем задачам видит все задачи
            queryset = queryset.all()
        elif user.user_role == user.UserRoleChoices.EMPLOYEE:
            queryset = queryset.filter(Q(employee=user) | Q(employee__isnull=True))

        return queryset
