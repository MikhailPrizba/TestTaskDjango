from rest_framework import viewsets, mixins, permissions
from .models import Customer, Employee, User
from .serializers import CustomerSerializer, EmployeeSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsEmployee, IsCustomer
from django.shortcuts import get_object_or_404


class AddCustomerView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для добавления нового клиента.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]


class AddEmployeeView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для добавления нового сотрудника.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]


class ProfileViewSet(viewsets.GenericViewSet):
    """
    ViewSet для управления профилем пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_customer(self, user):
        return get_object_or_404(Customer, pk=user.pk)

    def get_employee(self, user):
        return get_object_or_404(Employee, pk=user.pk)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        Возвращает данные профиля текущего пользователя.
        """
        user = request.user
        if user.user_role == User.UserRoleChoices.CUSTOMER:
            customer = self.get_customer(user)
            serializer = CustomerSerializer(customer)
        elif user.user_role == User.UserRoleChoices.EMPLOYEE:
            employee = self.get_employee(user)
            serializer = EmployeeSerializer(employee)
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data)


class ListEmployeeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для списка сотрудников.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]


class ListCustomerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для списка клиентов.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]
