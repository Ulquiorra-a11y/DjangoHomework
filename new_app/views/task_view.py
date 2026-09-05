from django.db.models.functions import ExtractWeekDay
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, \
    CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from new_app.models import Task, Statuses
from new_app.serializers.task import TaskSerializer, TaskDetailSerializer, TaskCreateSerializer
from django.db.models import Count, Q
from django.utils import timezone



WEEKDAY = {
    'sunday': 1,
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7
}

class TaskListView(ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        return TaskCreateSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        day_param = self.request.query_params.get('day')

        if not day_param:
            return queryset

        weekday_number = WEEKDAY.get(day_param.strip().lower())
        if weekday_number is None:
            raise ValidationError(f"Invalid day: '{day_param}'.")

        return queryset.annotate(
            deadline_weekday=ExtractWeekDay('deadline')
        ).filter(deadline_weekday=weekday_number)





class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer




class TaskStatistics(APIView):
    def get(self, request):
        now = timezone.now()
        stats = Task.objects.aggregate(
            total_count=Count('id'),
            overdue_count=Count('id', filter=Q(deadline__lt=now) & ~Q(status=Statuses.DONE)),
            **{f'{s.value}_count': Count('id', filter=Q(status=s.value)) for s in Statuses}
        )
        return Response(stats, status=status.HTTP_200_OK)