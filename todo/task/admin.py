from django.contrib import admin
from todo.task.models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'due_date', )
    list_display_links = ['name',]
    search_fields = ['name',]

admin.site.register(Task, TaskAdmin)