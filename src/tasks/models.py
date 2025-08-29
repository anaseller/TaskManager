from django.db import models

class Status(models.TextChoices):
    NEW = 'New', 'New'
    IN_PROGRESS = 'In progress', 'In progress'
    PENDING = 'Pending', 'Pending'
    BLOCKED = 'Blocked', 'Blocked'
    DONE = 'Done', 'Done'

class Category(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name

class Task(models.Model):

    title = models.CharField(
        max_length=200,
        unique_for_date='created_at'
    )
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SubTasks"

    def __str__(self):
        return self.title
