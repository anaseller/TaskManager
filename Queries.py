import os
import django
from django.db.models.query import QuerySet
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from src.tasks.models import Task, SubTask


def main():
    # Задача 1: Создание записей
    print("--- Создание записей ---")

    # Task
    task_presentation = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status="New",
        deadline=timezone.now() + timedelta(days=3)
    )
    print("Создана задача 'Подготовить презентацию'.")

    # SubTasks
    subtask_gather_info = SubTask.objects.create(
        task=task_presentation,
        title="Gather information",
        description="Find necessary information for the presentation",
        status="New",
        deadline=timezone.now() + timedelta(days=2)
    )
    print("Создана подзадача 'Собрать информацию'.")

    subtask_create_slides = SubTask.objects.create(
        task=task_presentation,
        title="Create slides",
        description="Create presentation slides",
        status="New",
        deadline=timezone.now() + timedelta(days=1)
    )
    print("Создана подзадача 'Создать слайды'.")

    # Задача 2: Чтение записей
    print("\n--- Чтение записей ---")
    # Задачи со статусом "New"
    new_tasks = Task.objects.filter(status="New")
    print("Задачи со статусом 'New':", new_tasks.count())
    for task in new_tasks:
        print(f"ID: {task.id}, Название: {task.title}, Статус: {task.status}")

    # Подзадачи с просроченным статусом "Done"
    # Для тестирования я изменила deadline на прошлую дату
    subtask_create_slides.deadline = timezone.now() - timedelta(days=1)
    subtask_create_slides.status = "Done"
    subtask_create_slides.save()

    overdue_done_subtasks = SubTask.objects.filter(
        status="Done",
        deadline__lt=timezone.now()
    )
    print("Просроченные подзадачи со статусом 'Done':", overdue_done_subtasks.count())
    for subtask in overdue_done_subtasks:
        print(f"ID: {subtask.id}, Название: {subtask.title}, Дедлайн: {subtask.deadline}")

    # Задача 3: Изменение записей
    print("\n--- Изменение записей ---")

    # Изменить статус "Prepare presentation" на "In progress"
    task_presentation.status = "In progress"
    task_presentation.save()
    print("Статус 'Prepare presentation' изменен на 'In progress'.")

    # Изменить срок выполнения для "Gather information" на два дня назад
    subtask_gather_info.deadline = timezone.now() - timedelta(days=2)
    subtask_gather_info.save()
    print("Срок выполнения для 'Gather information' изменен на два дня назад.")

    # Изменить описание для "Create slides"
    subtask_create_slides.description = "Create and format presentation slides"
    subtask_create_slides.save()
    print("Описание для 'Создать слайды' изменено.")

    # Задача 4: Удаление записей
    print("\n--- Удаление записей ---")

    # Удалить задачу "Prepare presentation" и все ее подзадачи
    task_presentation.delete()
    print("Задача 'Prepare presentation' и все ее подзадачи удалены.")

    # Проверка, что записи удалены
    if not Task.objects.filter(title="Prepare presentation").exists():
        print("Проверка: Задача 'Prepare presentation' успешно удалена.")
    if not SubTask.objects.filter(task__title="Prepare presentation").exists():
        print("Проверка: Подзадачи для 'Prepare presentation' успешно удалены.")


if __name__ == '__main__':
    main()
