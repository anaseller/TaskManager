from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskListCreateAPIView,
    TaskDetailAPIView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskListByDayOfWeekAPIView,
    CategoryViewSet
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),

    path('tasks/by-day/', TaskListByDayOfWeekAPIView.as_view(), name='task-list-by-day'),

    path('', include(router.urls)),
]