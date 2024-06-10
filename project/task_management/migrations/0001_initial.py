# Generated by Django 5.0.6 on 2024-06-10 08:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает исполнителя"),
                            ("in_progress", "В процессе"),
                            ("completed", "Выполнена"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("report", models.TextField(blank=True)),
            ],
            options={
                "permissions": [("view_all_tasks", "Can view all tasks")],
            },
        ),
    ]
