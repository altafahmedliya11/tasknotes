from rest_framework import serializers
from .models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_due_date(self, value):
        """
        Validates the due date of a task, ensuring it is not in the past.

        Raises:
            ValidationError: If the due date is in the past.
        """
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
