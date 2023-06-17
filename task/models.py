from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="workers",
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.position}({self.username})"


class Task(models.Model):
    PRIORITY_LEVEL_CHOICES = (
        ("L", "low"),
        ("M", "medium"),
        ("H", "high"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_LEVEL_CHOICES,
        default="medium",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=False,
        blank=False,
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["is_completed", "deadline", "priority"]
