from django.contrib import admin
from django.urls import path, include
from new_app.views.task_view import TaskList, TaskDetail, TaskStatistics
from new_app.views.subtask_views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list' ),
    path('tasks/<uuid:pk>/', TaskDetail.as_view(), name='task-detail' ),
    path('tasks/statistics/', TaskStatistics.as_view(), name='task-statistics'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list' ),
    path('subtasks/<uuid:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail' ),
]