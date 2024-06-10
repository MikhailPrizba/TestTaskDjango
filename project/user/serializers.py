# serializers.py
from rest_framework import serializers
from .models import Customer, Employee
from user.models import User
from .fields import Base64ImageFieldWithSwagger


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "password",
            "user_role",
        ]
        read_only_fields = ["id", "user_role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Создает нового пользователя с зашифрованным паролем.
        """
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Customer.
    """

    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "password",
            "user_role",
        ]
        read_only_fields = ["id", "user_role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Создает нового клиента с зашифрованным паролем и ролью клиента.
        """
        validated_data["user_role"] = User.UserRoleChoices.CUSTOMER
        user = Customer(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Employee.
    """

    photo = Base64ImageFieldWithSwagger()

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "password",
            "user_role",
            "photo",
        ]
        read_only_fields = ["id", "user_role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Создает нового сотрудника с зашифрованным паролем и ролью сотрудника.
        """
        validated_data["user_role"] = User.UserRoleChoices.EMPLOYEE
        user = Employee(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
