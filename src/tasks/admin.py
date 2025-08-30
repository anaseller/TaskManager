from django.contrib import admin
from .models import Task, SubTask, Category


# Инлайн-форма для подзадач
class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1


# Класс админки для задачи
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]

    # Метод для укороченного отображения заголовка
    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title

    short_title.short_description = 'Task Title'

    list_display = ('short_title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at')
    search_fields = ('title', 'description')


# Пользовательский action для подзадач
@admin.action(description="Отметить как Done")
def mark_as_done(modeladmin, request, queryset):
    queryset.update(status="Done")


# Класс админки для подзадачи
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    actions = [mark_as_done]


# Регистрация других моделей
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)