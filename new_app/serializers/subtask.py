from rest_framework import serializers
from new_app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at')


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at')