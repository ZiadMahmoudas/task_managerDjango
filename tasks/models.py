"""
tasks/models.py

The Task model is the core domain object of this application.
It is always tied to a specific User via a ForeignKey, which is the
foundation of our ownership-based access control.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):

    # ------------------------------------------------------------------
    # CHOICES
    # ------------------------------------------------------------------

    class Status(models.TextChoices):
        PENDING     = 'pending',     'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED   = 'completed',   'Completed'

    class Priority(models.TextChoices):
        LOW    = 'low',    'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH   = 'high',   'High'

    # ------------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------------

    # CASCADE ensures tasks are deleted when their owner is deleted.
    # related_name='tasks' allows user.tasks.all() in templates/views.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    # Optional due date — tasks don't require one
    due_date = models.DateField(null=True, blank=True)

    # auto_now_add: set once at creation; auto_now: updated on every save
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ------------------------------------------------------------------
    # META
    # ------------------------------------------------------------------

    class Meta:
        ordering = ['-created_at']  # Newest tasks first by default
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    # ------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------

    def __str__(self):
        return f'{self.title} ({self.user.username})'

    def get_absolute_url(self):
        return reverse('tasks:detail', kwargs={'pk': self.pk})

    # Convenience properties used in templates for Bootstrap badge colors
    @property
    def status_badge_class(self):
        return {
            self.Status.PENDING:     'warning',
            self.Status.IN_PROGRESS: 'info',
            self.Status.COMPLETED:   'success',
        }.get(self.status, 'secondary')

    @property
    def priority_badge_class(self):
        return {
            self.Priority.LOW:    'success',
            self.Priority.MEDIUM: 'warning',
            self.Priority.HIGH:   'danger',
        }.get(self.priority, 'secondary')

    @property
    def is_overdue(self):
        """Returns True if the task has a due date that has passed and is not completed."""
        from django.utils import timezone
        if self.due_date and self.status != self.Status.COMPLETED:
            return self.due_date < timezone.now().date()
        return False
