from django.db import models
from django_enum import TextChoices
from user.models import User


class Task(models.Model):
    class StatusChoices(TextChoices):
        PENDING = "pending", "Ожидает исполнителя"
        IN_PROGRESS = "in_progress", "В процессе"
        COMPLETED = "completed", "Выполнена"

    customer = models.ForeignKey(
        User, related_name="customer_tasks", on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        User,
        related_name="employee_tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    report = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.status == Task.StatusChoices.COMPLETED and not self.report:
            raise ValueError("Report cannot be empty when task is completed")
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("view_all_tasks", "Can view all tasks"),
        ]
