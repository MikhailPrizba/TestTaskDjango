import pytest
from django_dynamic_fixture import G
from rest_framework.test import APIClient
from user.models import User, Customer, Employee


@pytest.fixture
def customer():
    return G(Customer, user_role=User.UserRoleChoices.CUSTOMER)


@pytest.fixture
def employee():
    return G(Employee, user_role=User.UserRoleChoices.EMPLOYEE)


@pytest.fixture
def customer_client(customer):
    client = APIClient()
    client.force_authenticate(
        user=customer.user_ptr
    )  # Используем user_ptr для аутентификации
    return client


@pytest.fixture
def employee_client(employee):
    client = APIClient()
    client.force_authenticate(
        user=employee.user_ptr
    )  # Используем user_ptr для аутентификации
    return client
