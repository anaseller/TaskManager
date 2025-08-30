from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from .models import Task, SubTask
from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskDetailSerializer,
    SubTaskSerializer
)


class TaskCreateView(generics.CreateAPIView):
    """
    Эндпоинт для создания новой задачи
    """
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskListAPIView(generics.ListAPIView):
    """
    Эндпоинт для получения списка всех задач
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения конкретной задачи по ее id
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskStatisticsAPIView(APIView):
    """
    Эндпоинт для получения статистики задач
    """

    def get(self, request):
        total_tasks = Task.objects.count()
        tasks_by_status = Task.objects.values('status').annotate(count=Count('status'))

        overdue_tasks = Task.objects.filter(
            deadline__lt=timezone.now(),
            status__in=['New', 'In progress', 'Pending', 'Blocked']
        ).count()

        statistics = {
            'total_tasks': total_tasks,
            'tasks_by_status': list(tasks_by_status),
            'overdue_tasks': overdue_tasks
        }
        return Response(statistics)

class SubTaskListCreateView(generics.ListCreateAPIView):
    """
    Эндпоинт для создания подзадачи и получения списка всех подзадач
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпоинт для получения, обновления и удаления конкретной подзадачи
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'

