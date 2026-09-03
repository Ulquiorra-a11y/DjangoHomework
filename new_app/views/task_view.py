from django.db.models.functions import ExtractWeekDay
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView,ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from new_app.models import Task, Statuses
from new_app.serializers.task import TaskSerializer,TaskDetailSerializer
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

class TaskListView(ListAPIView):
    serializer_class = TaskSerializer

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


class TaskDetailView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'pk'


class TaskDetail(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskStatistics(APIView):
    def get(self, request):
        now = timezone.now()
        stats = Task.objects.aggregate(
            total_count=Count('id'),
            overdue_count=Count('id', filter=Q(deadline__lt=now) & ~Q(status=Statuses.DONE)),
            **{f'{s.value}_count': Count('id', filter=Q(status=s.value)) for s in Statuses}
        )
        return Response(stats, status=status.HTTP_200_OK)