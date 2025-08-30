from django.urls import path
from .views import (
    TaskListCreateAPIView,
    TaskDetailAPIView,
    SubTaskListCreateAPIView,
    SubTaskDetailUpdateDeleteAPIView,
    TaskStatisticsAPIView,
    TaskListByDayView,
)

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteAPIView.as_view(), name='subtask-detail'),

    path('tasks/statistics/', TaskStatisticsAPIView.as_view(), name='task-statistics'),
    path('tasks/by-day/', TaskListByDayView.as_view(), name='task-list-by-day'),
]