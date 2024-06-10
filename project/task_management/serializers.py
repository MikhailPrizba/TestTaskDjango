from rest_framework import serializers
from .models import Task
from user.models import Customer
from datetime import datetime as dt


class TaskCreateByCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["customer"] = request.user
        return super().create(validated_data)


class TaskCreateByEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "customer"]

    def validate_customer(self, value):
        # Ensure the customer exists and is valid
        if not Customer.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("The specified customer does not exist.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["employee"] = request.user
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "customer",
            "employee",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
            "closed_at",
            "report",
        ]
        read_only_fields = [
            "id",
            "status",
            "report",
            "customer",
            "employee",
        ]

    def validate(self, data):
        # Если задача уже завершена, запрещаем любые изменения
        if self.instance and self.instance.status == Task.StatusChoices.COMPLETED:
            raise serializers.ValidationError("Completed tasks cannot be edited.")
        if (
            self.instance
            and self.instance.employee
            and self.context["request"].user != self.instance.employee
        ):
            raise serializers.ValidationError(
                "Only the assigned employee can edit this task."
            )

        return data


class TaskTakeSerializer(serializers.ModelSerializer):
    employee = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=Task.StatusChoices.IN_PROGRESS)

    class Meta:
        model = Task
        fields = ["employee", "status"]

    def validate(self, data):
        # Ensure the task is not already completed
        if self.instance and self.instance.status == Task.StatusChoices.COMPLETED:
            raise serializers.ValidationError("Completed tasks cannot be edited.")

        # Ensure the task is not already assigned to an employee
        if self.instance and self.instance.employee is not None:
            raise serializers.ValidationError(
                "This task is already assigned to an employee."
            )

        return data

    def update(self, instance, validated_data):
        instance.employee = self.context["request"].user
        instance.status = Task.StatusChoices.IN_PROGRESS
        instance.save()
        return instance


class TaskCloseSerializer(serializers.ModelSerializer):
    report = serializers.CharField(required=True)
    employee = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default=Task.StatusChoices.COMPLETED)
    closed_at = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(dt.utcnow)
    )

    class Meta:
        model = Task
        fields = [
            "report",
            "employee",
            "status",
            "closed_at",
        ]

    def validate(self, data):
        # Ensure the employee is the one closing the task
        if self.instance.employee != self.context["request"].user:
            raise serializers.ValidationError(
                "You can only close tasks assigned to you."
            )

        # Ensure the task is not already completed
        if self.instance.status == Task.StatusChoices.COMPLETED:
            raise serializers.ValidationError("Completed tasks cannot be edited.")

        return data

    def update(self, instance, validated_data):
        instance.status = Task.StatusChoices.COMPLETED
        instance.report = validated_data.get("report")
        instance.closed_at = dt.utcnow()
        instance.save()
        return instance
