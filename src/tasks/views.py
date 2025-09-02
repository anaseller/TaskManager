from rest_framework import status, generics, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractWeekDay
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
    UserRegistrationSerializer
)
from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnly


WEEKDAY_MAPPING = {
    'понедельник': 1,
    'вторник': 2,
    'среда': 3,
    'четверг': 4,
    'пятница': 5,
    'суббота': 6,
    'воскресенье': 7,
}

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            response.set_cookie('access', access_token, httponly=True)
            response.set_cookie('refresh', refresh_token, httponly=True)
            return response
        return response

class UserRegistrationView(APIView):
    permission_classes = []  # Разрешен доступ без аутентификации

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "The user has been successfully registered.", "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response

        except TokenError:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпоинт для получения, обновления и удаления конкретной задачи по ее id
    """
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class TaskListByDayOfWeekAPIView(generics.ListAPIView):
    """
    Эндпоинт для получения списка задач по дню недели.
    """
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для CRUD операций с категориями и подсчета количества задач
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):

        categories_with_task_count = Category.objects.annotate(task_count=Count('tasks')).values('id', 'name', 'task_count')
        return Response(categories_with_task_count)

class CurrentUserTasksAPIView(generics.ListAPIView):
    """
    Получение списка задач, принадлежащих только текущему пользователю
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Фильтруем задачи по текущему пользователю
        return Task.objects.filter(owner=self.request.user).order_by('-created_at')
