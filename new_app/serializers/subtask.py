from rest_framework import serializers
from new_app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at', 'task_title', 'owner')


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at','owner')
        read_only_fields = ('id', 'created_at', 'owner')