from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractWeekDay
from django.db.models import Count, Q
from django.utils import timezone
from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer
)
from .pagination import StandardResultsSetPagination

WEEKDAY_MAPPING = {
    'понедельник': 1,
    'вторник': 2,
    'среда': 3,
    'четверг': 4,
    'пятница': 5,
    'суббота': 6,
    'воскресенье': 7,
}


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    Эндпоинт для создания новой задачи и получения списка всех задач
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпоинт для получения, обновления и удаления конкретной задачи по ее id
    """
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'


class SubTaskListCreateAPIView(generics.ListCreateAPIView):
    """
    Эндпоинт для создания подзадачи и получения списка всех подзадач
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпоинт для получения, обновления и удаления конкретной подзадачи
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
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


class TaskListByDayView(generics.ListAPIView):
    """
    Эндпоинт для получения списка задач по дню недели
    """
    serializer_class = TaskSerializer
    def get_queryset(self):
        queryset = Task.objects.all()
        day_of_week = self.request.query_params.get('day_of_week', None)
        if day_of_week:
            try:
                day_num = WEEKDAY_MAPPING[day_of_week.lower()]
                queryset = queryset.annotate(
                    weekday=ExtractWeekDay('created_at')
                ).filter(weekday=day_num)
            except KeyError:
                return Task.objects.none()
        return queryset


class SubTaskListCreateView(generics.ListCreateAPIView):
    """
    Эндпоинт для создания подзадачи и получения списка всех подзадач с пагинацией и фильтрацией
    """
    serializer_class = SubTaskSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = SubTask.objects.order_by('-created_at')
        task_title_param = self.request.query_params.get('task_title', None)
        subtask_status_param = self.request.query_params.get('subtask_status', None)

        if task_title_param:
            queryset = queryset.filter(task__title__icontains=task_title_param)
        if subtask_status_param:
            queryset = queryset.filter(status__icontains=subtask_status_param)

        return queryset


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпоинт для получения, обновления и удаления конкретной подзадачи
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'

