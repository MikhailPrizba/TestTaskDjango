import pytest
from django.urls import reverse
from rest_framework import status
from task_management.models import Task
from ddf import G
from user.models import Customer, Employee
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestTaskViews:
    def test_create_task_by_customer(self, customer_client: APIClient) -> None:
        task_data = {"title": "Test Task", "description": "Test Description"}
        url = reverse("customer-create-task-list")

        response = customer_client.post(url, task_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.filter(title=task_data["title"]).exists()

    def test_create_task_by_employee(self, employee_client: APIClient) -> None:
        customer = G(Customer, user_role=Customer.UserRoleChoices.CUSTOMER)
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "customer": customer.id,
        }
        url = reverse("employee-create-task-list")

        response = employee_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.filter(title=task_data["title"]).exists()

    def test_get_task(self, customer_client: APIClient, customer: Customer) -> None:
        task = G(Task, customer=customer)
        url = reverse("task-detail", args=[task.id])

        response = customer_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_task(self, employee_client: APIClient, employee: Employee) -> None:
        task = G(Task, employee=employee)
        task_data = {"title": "Updated Task Title", "description": task.description}
        url = reverse("task-detail", args=[task.id])

        response = employee_client.put(url, task_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Task.objects.filter(title="Updated Task Title").exists()

    def test_take_task(self, employee_client: APIClient, employee: Employee) -> None:
        task = G(Task)
        url = reverse("employee-actions-take-task", args=[task.id])

        response = employee_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status == Task.StatusChoices.IN_PROGRESS
        assert task.employee.id == employee.id

    def test_close_task(self, employee_client: APIClient, employee: Employee) -> None:
        task = G(Task, employee=employee, status=Task.StatusChoices.IN_PROGRESS)
        url = reverse("employee-actions-close-task", args=[task.id])
        data = {"report": "Task completed successfully."}

        response = employee_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status == Task.StatusChoices.COMPLETED
        assert task.report == data["report"]

    def test_permission_customer_can_only_see_own_tasks(
        self, customer_client: APIClient, customer: Customer, employee: Employee
    ) -> None:
        customer_task = G(Task, customer=customer)
        other_customer_task = G(Task, customer=employee)
        url = reverse("task-list")

        response = customer_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        task_ids = [task["id"] for task in response.data]
        assert customer_task.id in task_ids
        assert other_customer_task.id not in task_ids

    def test_permission_employee_can_see_all_tasks(
        self, employee_client: APIClient, customer: Customer, employee: Employee
    ) -> None:
        customer_task = G(Task, customer=customer)
        employee_task = G(Task, customer=customer, employee=employee)
        url = reverse("task-list")

        response = employee_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        task_ids = [task["id"] for task in response.data]
        assert customer_task.id in task_ids
        assert employee_task.id in task_ids

    def test_filter_customer_cannot_update_other_customers_task(
        self, customer_client: APIClient, customer: Customer, employee: Employee
    ) -> None:
        other_customer_task = G(Task, customer=employee)
        url = reverse("task-detail", args=[other_customer_task.id])
        data = {"title": "Updated Title"}

        response = customer_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        other_customer_task.refresh_from_db()
        assert other_customer_task.title != "Updated Title"

    def test_permission_employee_can_update_own_assigned_task(
        self, employee_client: APIClient, employee: Employee
    ) -> None:
        task = G(Task, employee=employee)
        url = reverse("task-detail", args=[task.id])
        data = {"title": "Updated Title"}

        response = employee_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.title == "Updated Title"
