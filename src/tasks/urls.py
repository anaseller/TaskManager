from django.urls import path
from .views import (
    TaskCreateView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskStatisticsAPIView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskListByDayView,
)

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('', TaskListAPIView.as_view(), name='task-list'),
    path('<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('statistics/', TaskStatisticsAPIView.as_view(), name='task-statistics'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('tasks-by-day/', TaskListByDayView.as_view(), name='tasks-by-day'),
]
