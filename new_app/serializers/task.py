from django.utils import timezone
from rest_framework import serializers

from new_app.models import Task
from new_app.serializers.subtask import SubTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title', 'description', 'status', 'deadline')

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status','created_at', 'deadline',  'subtasks')


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at')

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Deadline can not be in the past!')
        return value