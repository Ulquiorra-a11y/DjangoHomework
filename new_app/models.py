import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.TextChoices):
    NEW = 'new', _('New')
    IN_PROGRESS = 'in_progress', _('In progress')
    PENDING = 'pending', _('Pending')
    BLOCKED = 'blocked', _('Blocked')
    DONE = 'done', _('Done')


class UniqueID(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4,
                          verbose_name='UUID id')

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Deleted at'))

    class Meta:
        abstract = True


class Category(UniqueID, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Category name'))

    def __str__(self):
        return f'Category: {self.name}'

    def __repr__(self):
        return f'<Category(name={self.name})>'

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Task(UniqueID, TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True, verbose_name=_('Categories'))
    status = models.CharField(max_length=15, choices=Statuses, default=Statuses.NEW,
                              verbose_name=_('Status'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    def __str__(self):
        return f'Task: {self.title}'

    def __repr__(self):
        return (f'<Task(title={self.title}, description={self.description}, status={self.status},'
                f'deadline={self.deadline})>')

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('-created_at',)


class SubTask(UniqueID, TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name=_('Task'))
    status = models.CharField(max_length=15, choices=Statuses, default=Statuses.NEW,
                              verbose_name=_('Status'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    def __str__(self):
        return f'SubTask: {self.title} ({self.task.title})'

    def __repr__(self):
        return (f'<SubTask(title={self.title}, description={self.description}, status={self.status},'
                f'deadline={self.deadline}, task={self.task})>')

    class Meta:
        db_table = 'subtasks'
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        ordering = ('-created_at',)
        unique_together = ('title', 'task')


from django.db import models

# Create your models here.
