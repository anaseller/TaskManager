from django.contrib import admin
from .models import Task, SubTask, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'categories', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'task', 'created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
