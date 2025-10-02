import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Unique constraint
    department = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.department})"


class Task(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="tasks"
    )
    completed_at = models.DateTimeField(null=True, blank=True)  # Auto-set on completion

    def clean(self):
        """
        Validates the due date of a task, ensuring it is not in the past.

        Raises:
            ValidationError: If the due date is in the past.
        """
        # Rule: due date cannot be in the past
        if self.due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")

    def save(self, *args, **kwargs):
        # Rule: auto-set completed_at when marked Completed
        """
        Saves the task instance to the database.

        Automatically sets the completed_at field to the current timestamp
        when the task status is set to "Completed". If the task status
        is set to anything other than "Completed", the completed_at field
        is set to None.

        """
        if self.status == "Completed" and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != "Completed":
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} → {self.status}"
