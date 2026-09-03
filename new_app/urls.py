from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from new_app.views.task_view import TaskListView, TaskDetailView, TaskStatistics
from new_app.views.subtask_views import SubTaskListCreateView, SubTaskDetailView
from new_app.views.category_views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', TaskListView.as_view(), name='task-list' ),
    path('tasks/<uuid:pk>/', TaskDetailView.as_view(), name='task-detail' ),
    path('tasks/statistics/', TaskStatistics.as_view(), name='task-statistics'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list' ),
    path('subtasks/<uuid:pk>/', SubTaskDetailView.as_view(), name='subtask-detail' ),

]