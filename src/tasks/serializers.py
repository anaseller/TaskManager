from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError as DjangoValidationError


class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'


class SubTaskCreateSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'\


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


class TaskSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'\


class TaskCreateSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        allow_empty=True,
        required=False
    )

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

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
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="A user with this email already exists.")]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="A user with this username already exists.")]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        # Проверяем пароль на соответствие минимальным требованиям
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user