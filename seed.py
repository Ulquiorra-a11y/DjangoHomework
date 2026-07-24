
import os
from datetime import timedelta

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoHomework.settings'
django.setup()

from django.utils import timezone

from new_app.models import Task, SubTask, Statuses


# def create_records():
#     today = timezone.now()
#     task = Task.objects.create(title="Prepare presentation",
#                                description="Prepare materials and slides for the presentation",status=Statuses.NEW,
#                                deadline=today + timedelta(days=3))
#     subtasks_data = [{"title": "Gather information",
#                       "description": "Find necessary information for the presentation",
#                       "status": Statuses.NEW,
#                       "deadline": today + timedelta(days=2)},
#                      {"title": "Create slides",
#                       "description": "Create presentation slides",
#                       "status": Statuses.NEW,
#                       "deadline": today + timedelta(days=1)}]
#
#     for data in subtasks_data:
#         SubTask.objects.create(task=task, **data)
#
#     return task


# def read_records():
#     for t in Task.objects.filter(status=Statuses.NEW):
#         print(" -", t)
#
#     for st in SubTask.objects.filter(status=Statuses.DONE, deadline__lt=timezone.now()):
#         print(" -", st)


# def update_records():
#     updates = [
#         (Task, "Prepare presentation", {"status": Statuses.IN_PROGRESS}),
#         (SubTask, "Gather information", {"deadline": timezone.now() - timedelta(days=2)}),
#         (SubTask, "Create slides", {"description": "Create and format presentation slides"})]
#
#     for model, title, fields in updates:
#         obj = model.objects.get(title=title)
#         for field_name, value in fields.items():
#             setattr(obj, field_name, value)
#         obj.save()



def delete_records():
    task = Task.objects.get(title="Prepare presentation")
    deleted_count, deleted_details = task.delete()
    print(f"\nDeleted items: {deleted_count}, details: {deleted_details}")


# create_records()
# read_records()
# update_records()
delete_records()
