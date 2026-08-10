from django.contrib import admin

from new_app.models import Category, SubTask, Task, Statuses


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

    @admin.display(description='Title')
    def short_title(self, object):
        if len(object.title) > 10:
            return f'{object.title[:10]}...'
        return object.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    autocomplete_fields = ['task']

    @admin.action(description="Set SubTask's status to DONE")
    def status(self, queryset):
        queryset.update(status=Statuses.DONE)

    actions = [status]
