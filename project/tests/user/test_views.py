import pytest
from django.urls import reverse
from rest_framework import status
from user.models import Customer, Employee, User
from rest_framework.test import APIClient
from ddf import G


@pytest.mark.django_db
class TestUserViews:
    @pytest.fixture
    def url_add_customer(self):
        return reverse("add-customer-list")

    @pytest.fixture
    def url_add_employee(self):
        return reverse("add-employee-list")

    @pytest.fixture
    def url_profile(self):
        return reverse("profile-me")

    @pytest.fixture
    def url_list_employees(self):
        return reverse("list-employees-list")

    @pytest.fixture
    def url_list_customers(self):
        return reverse("list-customers-list")

    @pytest.fixture
    def customer_data(self):
        return {
            "username": "customer",
            "first_name": "Customer",
            "last_name": "Test",
            "email": "customer@example.com",
            "phone": "+1234567890",
            "password": "customerpassword",
        }

    @pytest.fixture
    def employee_data(self):
        return {
            "username": "employee",
            "first_name": "Employee",
            "last_name": "Test",
            "email": "employee@example.com",
            "phone": "+1234567891",
            "password": "employeepassword",
            "photo": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhISEhISEhISFhUVFRUVFRUVFRUVFRUWFhUVFRUYHSggGBolHRUVITEhJSkrLi4uFx8zODMsNygtLisBCgoKDg0OGxAQGy0lICYtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAKgBLAMBIgACEQEDEQH/xAAcAAACAwEBAQEAAAAAAAAAAAAABgIDBAUHAQj/xAA/EAACAQIEAgcEAwcFAAAAAAABAgADEQQSITEFQVFhBhMicYGRobHB0RQVI0JSI0KSwUOxFiMzgpLw/8QAGQEAAwEBAQAAAAAAAAAAAAAAAAECAwQF/8QAHREBAQEBAQACAwAAAAAAAAAAAAERAiExQWGx4f/aAAwDAQACEQMRAD8A6XiKKKACgAlqICiqIgICgBiaAAooAKCiIoAKAM0tRbSbErv6ntMSBfwrg2u9aHbRsJNdJWQ7Xhvyi2WPoFT0+ajwTc9W6nEkMKqDOR8DH9+tKt4T7acgx9LaEDSTcqWevYgOp5/9DVPS17zovRrNisLqrhT2lxCrXgjOBGT6kZPoaA4m2FIEt4LN9uIIvCZ5sQ1mB0DHxzQLE1ZbLB2uxt5YeZcbQNATuI+JFAmEDOS+9K8PvFCRABrOABJNa9o4N4HFwRo45myeV3Gc8gHiPTB9xzQyWWDHRZps1f/iy8N0PK5ji1mP7HZwycZC46CQR+ZqtVyrhbNE+zA5u+KsTj5wACCDn61ZFdDMXWYZ5I2kVnB4UgfZmXbllZkMDpzxwNUWZ4Vb2K92KKbtI6ELmD5P3lh+b0yMwQPWpWTbCGcQSy1u+7nFs1CW4cYjBzz8vaqLuotRBVo7W8GxeBtSyLqMEpUA6gi+pIHrScTItNnX1kmZKcShmtitJbNm8c0BlcA4riN8lU4P3e49ySMqHmrINHht3mNW5DN8gzFJGO2fLc9k3yDNGpp0nFwklzxy2fFe6MFBJGVuMnp1HGCCDx61y1yGQNLfN20aSHXgYnrEAA+wzj+lWsWI2kMRQDQAAUAQBAIAAFRoGklz8QaRATt5jaGwnJH6C+gpMNWjRy3RmVtYt0sTT7pgnR2vJwPPoA3zt3Hzrxkx0rDbUawspuTwx32ii5WxzTGkj5OfIjtPXXddDS9St2m7t5cxKgZljXBxnAoHj4/U8A6xy1hp9Hmt9PbTS1kBHV9aQQ2+J3eFZ4flXzA9SfrUqA2HSbZxuUZsBcL4UiZpkuA2Z9GI5G22Nhj5cfY0XStDV4f2lyoJQt+uxTMCySBGQMkkgYIXiCOSTqa1dXEKmOPhwi2a2ZhkT2aHMcLHiGP+",
        }

    def test_get_profile(self, customer_client: APIClient, url_profile: str):
        response = customer_client.get(url_profile)
        assert response.status_code == status.HTTP_200_OK

    def test_list_employees(self, customer_client: APIClient, url_list_employees: str):
        employees = [G(Employee) for _ in range(5)]
        response = customer_client.get(url_list_employees)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_list_customers(self, employee_client: APIClient, url_list_customers: str):
        customers = [G(Customer) for _ in range(5)]
        response = employee_client.get(url_list_customers)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_customer_cannot_add_employee(
        self, customer_client: APIClient, employee_data: dict, url_add_employee: str
    ):
        response = customer_client.post(url_add_employee, employee_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
