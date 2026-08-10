from django.contrib import admin
from django.urls import path, include
from new_app.views.task_view import TaskList, TaskDetail, TaskStatistics

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list' ),
    path('tasks/<uuid:pk>/', TaskDetail.as_view(), name='task-detail' ),
    path('tasks/statistics/', TaskStatistics.as_view(), name='task-statistics')
]