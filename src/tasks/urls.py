from django.urls import path
from .views import (
    TaskCreateView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskStatisticsAPIView
)

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('', TaskListAPIView.as_view(), name='task-list'),
    path('<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('statistics/', TaskStatisticsAPIView.as_view(), name='task-statistics'),
]