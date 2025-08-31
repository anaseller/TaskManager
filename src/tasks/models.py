from django.db import models
from django.conf import settings
from django.utils import timezone


class Status(models.TextChoices):
    NEW = 'New', 'New'
    IN_PROGRESS = 'In progress', 'In progress'
    PENDING = 'Pending', 'Pending'
    BLOCKED = 'Blocked', 'Blocked'
    DONE = 'Done', 'Done'


# Менеджер для мягкого удаления
class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveCategoryManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:

        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Task(models.Model):

    title = models.CharField(
        max_length=200,
        unique=True
    )
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='tasks')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:

        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class SubTask(models.Model):

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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

    def __str__(self):
        return self.title

    class Meta:

        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'