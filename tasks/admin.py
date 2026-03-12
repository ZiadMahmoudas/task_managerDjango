"""
tasks/admin.py

Rich admin configuration for the Task model.
Admins can filter by status/priority/due date and search by title.
"""

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'status', 'priority', 'due_date', 'created_at')
    list_filter   = ('status', 'priority', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
