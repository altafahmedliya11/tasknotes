from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee, Task
from django.utils import timezone
import uuid


class EmployeeTaskAPITestCase(APITestCase):

    def setUp(self):
        # Create an employee
        self.employee = Employee.objects.create(
            name="Altaf Ahmed", email="altaf@example.com", department="Engineering"
        )

        # Create a task assigned to employee
        self.task = Task.objects.create(
            title="Initial Task",
            description="Test task",
            due_date=timezone.now().date() + timezone.timedelta(days=5),
            status="Pending",
            assigned_to=self.employee,
        )

    # ----------------- Employee Tests -----------------
    def test_create_employee(self):
        url = reverse("employee-list")
        data = {
            "name": "Test Employee",
            "email": "test@example.com",
            "department": "HR",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(
            Employee.objects.get(email="test@example.com").name, "Test Employee"
        )

    # ----------------- Task Tests -----------------
    def test_create_task(self):
        url = reverse("task-list")
        data = {
            "title": "New Task",
            "description": "Task description",
            "due_date": str(timezone.now().date() + timezone.timedelta(days=3)),
            "status": "Pending",
            "assigned_to": str(self.employee.id),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(title="New Task").assigned_to, self.employee)

    def test_list_tasks_filter_by_status(self):
        url = reverse("task-list") + "?status=Pending"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        self.assertEqual(response.data[0]["status"], "Pending")


    def test_list_tasks_filter_by_employee(self):
        url = reverse("task-list") + f"?employee_id={self.employee.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check assigned_to matches the employee UUID
        for task in response.data:
            self.assertEqual(task["assigned_to"], self.employee.id)

    def test_update_task_description(self):
        url = reverse("task-detail", args=[str(self.task.id)])
        data = {"description": "Updated description"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.description, "Updated description")

    def test_update_task_status_completed(self):
        url = reverse("task-detail", args=[str(self.task.id)])
        data = {"status": "Completed"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "Completed")
        self.assertIsNotNone(self.task.completed_at)

    def test_delete_task(self):
        url = reverse("task-detail", args=[str(self.task.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
