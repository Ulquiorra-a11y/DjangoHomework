from rest_framework import serializers

from new_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id','title', 'description', 'status', 'deadline')