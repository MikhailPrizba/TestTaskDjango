from rest_framework.permissions import BasePermission
from user.models import User


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        """
        Проверка, является ли пользователь сотрудником.
        """
        return request.user.user_role == User.UserRoleChoices.EMPLOYEE


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        """
        Проверка, является ли пользователь клиентом.
        """
        return request.user.user_role == User.UserRoleChoices.CUSTOMER


class IsTaskEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверка, является ли пользователь назначенным сотрудником для задачи.
        """
        return request.user == obj.employee


class IsTaskCustomerOrEmployee(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверка, имеет ли пользователь права доступа к задаче как клиент или сотрудник.
        """
        # Разрешение на просмотр задачи клиентом, сотрудником или пользователем с правами просмотра всех задач
        if view.action in ["retrieve", "list"]:
            return (
                request.user == obj.customer
                or request.user == obj.employee
                or request.user.has_perm("task_management.view_all_tasks")
            )
        # Разрешение на обновление задачи клиентом или сотрудником
        if view.action in ["update", "partial_update"]:
            return request.user == obj.customer or request.user == obj.employee
        return False
