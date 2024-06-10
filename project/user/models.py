from django.contrib.auth.models import AbstractUser
from django.db import models
from django_enum import TextChoices


class User(AbstractUser):
    class UserRoleChoices(TextChoices):
        EMPLOYEE = "EMPLOYEE"
        CUSTOMER = "CUSTOMER"

    user_role = models.TextField(choices=UserRoleChoices.choices)
    middle_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, unique=True)


class Customer(User):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Employee(User):
    photo = models.ImageField(upload_to="employee_photos/", blank=False)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
