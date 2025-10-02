from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employee, Task
from .serializers import EmployeeSerializer, TaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Returns a filtered queryset of tasks based on query parameters.

        Query parameters:
            status (str): filter by task status
            employee_id (int): filter by employee id

        Returns:
            Queryset: filtered queryset of tasks
        """
        queryset = Task.objects.all()
        status = self.request.query_params.get("status")
        employee_id = self.request.query_params.get("employee_id")

        if status:
            queryset = queryset.filter(status=status)
        if employee_id:
            queryset = queryset.filter(assigned_to__id=employee_id)

        return queryset
