from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TaskListCreateAPIView,
    TaskDetailAPIView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskListByDayOfWeekAPIView,
    CategoryViewSet,
    CurrentUserTasksAPIView,
    UserRegistrationView,
    CustomTokenObtainPairView,
    UserLogoutView
)


schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API documentation for the Task Manager project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),

    path('tasks/by-day/', TaskListByDayOfWeekAPIView.as_view(), name='task-list-by-day'),
    path('tasks/my_tasks/', CurrentUserTasksAPIView.as_view(), name='my-tasks'),

    path('', include(router.urls)),

    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]