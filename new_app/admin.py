from django.contrib import admin

from new_app.models import Category, SubTask, Task


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0
    fields = ('title', 'status', 'deadline')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    date_hierarchy = ('deadline')
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    autocomplete_fields = ['task']


from django.contrib import admin

# Register your models here.
