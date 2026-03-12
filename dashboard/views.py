"""
dashboard/views.py

Admin-only views. Every view here inherits StaffRequiredMixin, which
guarantees that only is_staff or is_superuser users can access these pages.

These views query across ALL users (no .filter(user=request.user) constraint)
because admins are meant to have a system-wide view.
"""

from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.db.models import Count, Q

from tasks.models import Task
from .mixins import StaffRequiredMixin


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    """
    System-wide statistics overview for admin users.
    Shows totals, recent users, and recent tasks.
    """
    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Aggregate task counts by status in one DB query
        task_stats = Task.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status=Task.Status.PENDING)),
            in_progress=Count('id', filter=Q(status=Task.Status.IN_PROGRESS)),
            completed=Count('id', filter=Q(status=Task.Status.COMPLETED)),
        )

        context['total_users']       = User.objects.count()
        context['total_tasks']       = task_stats['total']
        context['pending_tasks']     = task_stats['pending']
        context['in_progress_tasks'] = task_stats['in_progress']
        context['completed_tasks']   = task_stats['completed']

        # Recent activity feeds
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        context['recent_tasks'] = Task.objects.select_related('user').order_by('-created_at')[:10]

        return context


class AdminUserListView(StaffRequiredMixin, ListView):
    """
    Lists all registered users with their task counts.
    annotate() adds task_count without N+1 queries.
    """
    model = User
    template_name = 'dashboard/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return (
            User.objects
            .annotate(task_count=Count('tasks'))
            .order_by('-date_joined')
        )


class AdminTaskListView(StaffRequiredMixin, ListView):
    """
    Lists all tasks across all users.
    select_related('user') avoids N+1 queries when accessing task.user in templates.
    """
    model = Task
    template_name = 'dashboard/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = Task.objects.select_related('user').order_by('-created_at')

        # Optional search and filter for admins too
        search   = self.request.GET.get('search', '').strip()
        status   = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')

        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(user__username__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from tasks.forms import TaskFilterForm
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        return context
