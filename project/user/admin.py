from django.contrib import admin
from .models import Customer, Employee, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    """
    Кастомный админ для модели User, с особыми настройками для добавления пользователей.
    """

    # Указываем поля, которые должны быть видимыми при добавлении нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "phone",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        Устанавливает роль пользователя при создании нового объекта.
        """
        if not change:  # Если это создание нового объекта
            if isinstance(obj, Customer):
                obj.user_role = User.UserRoleChoices.CUSTOMER
            elif isinstance(obj, Employee):
                obj.user_role = User.UserRoleChoices.EMPLOYEE
        super().save_model(request, obj, form, change)


class CustomerAdmin(CustomUserAdmin):
    """
    Админ для модели Customer, с особыми настройками полей.
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Role", {"fields": ("user_role",)}),
    )


class EmployeeAdmin(CustomUserAdmin):
    """
    Админ для модели Employee, с особыми настройками полей.
    """

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "phone",
                    "photo",  # Добавляем поле photo сюда
                ),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "phone",
                    "photo",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Role", {"fields": ("user_role",)}),
    )


# Регистрируем модели в админке
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
