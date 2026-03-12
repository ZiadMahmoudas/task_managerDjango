"""
tasks/views.py

All views in this module are protected by LoginRequiredMixin.

Security principle: Every queryset is filtered by request.user.
A user can NEVER access, edit, or delete another user's task because
we always chain .filter(user=request.user) before any lookup.

Class-based views are used throughout for consistency and to leverage
built-in pagination, form handling, and success URL logic.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView,
)

from .models import Task
from .forms import TaskForm, TaskFilterForm


class UserDashboardView(LoginRequiredMixin, TemplateView):
    """
    Personal dashboard showing task summary statistics for the logged-in user.
    """
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(user=self.request.user)

        context['total_tasks']      = user_tasks.count()
        context['pending_tasks']    = user_tasks.filter(status=Task.Status.PENDING).count()
        context['in_progress_tasks']= user_tasks.filter(status=Task.Status.IN_PROGRESS).count()
        context['completed_tasks']  = user_tasks.filter(status=Task.Status.COMPLETED).count()
        context['high_priority']    = user_tasks.filter(priority=Task.Priority.HIGH).count()
        context['recent_tasks']     = user_tasks[:5]  # 5 most recently created
        return context


class TaskListView(LoginRequiredMixin, ListView):
    """
    Lists all tasks belonging to the logged-in user.
    Supports search by title/description and filtering by status and priority.
    """
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        """
        Always scoped to request.user — users cannot see each other's tasks.
        GET parameters drive the optional search and filter behavior.
        """
        queryset = Task.objects.filter(user=self.request.user)

        search  = self.request.GET.get('search', '').strip()
        status  = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pre-populate the filter form with the current GET params
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Shows full details for a single task.
    get_queryset scopes to the current user — a 404 is returned if
    another user's task ID is guessed in the URL.
    """
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Creates a new task for the logged-in user.
    We override form_valid to attach request.user before saving.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        # Assign ownership before saving to the database
        form.instance.user = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Task'
        context['submit_label'] = 'Create Task'
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edits an existing task.
    get_queryset ensures users can only edit their own tasks.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Task'
        context['submit_label'] = 'Save Changes'
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Confirms and deletes a task.
    get_queryset scopes deletion to the owner — a 404 is returned
    if a user tries to delete someone else's task.
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Task deleted.')
        return super().form_valid(form)
