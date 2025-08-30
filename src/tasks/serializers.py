from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone


class SubTaskSerializer(serializers.ModelSerializer):


    class Meta:
        model = SubTask
        fields = '__all__'


class SubTaskCreateSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        # Проверка уникальности имени категории
        instance = self.instance
        if Category.objects.filter(name=value).exclude(pk=getattr(instance, 'pk', None)).exists():
            raise serializers.ValidationError("Категория с таким именем уже существует")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        allow_empty=True,
        required=False
    )

    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        # Проверка, что дата дедлайна не в прошлом
        if value and value < timezone.now():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом")
        return value


class TaskDetailSerializer(serializers.ModelSerializer):

    subtasks = SubTaskSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'