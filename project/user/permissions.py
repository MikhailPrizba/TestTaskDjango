from rest_framework.permissions import BasePermission
from user.models import User


class IsEmployee(BasePermission):
    """
    Разрешение, проверяющее, является ли пользователь сотрудником.
    """

    def has_permission(self, request, view):
        """
        Проверка, является ли пользователь сотрудником.
        """
        return request.user.user_role == User.UserRoleChoices.EMPLOYEE


class IsCustomer(BasePermission):
    """
    Разрешение, проверяющее, является ли пользователь клиентом.
    """

    def has_permission(self, request, view):
        """
        Проверка, является ли пользователь клиентом.
        """
        return request.user.user_role == User.UserRoleChoices.CUSTOMER
