"""
tasks/urls.py

URL patterns for the user-facing task management interface.
All routes in this file require authentication (enforced via LoginRequiredMixin in views).
"""

from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # User's personal dashboard (summary + recent tasks)
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),

    # Task CRUD
    path('',           views.TaskListView.as_view(),   name='list'),
    path('create/',    views.TaskCreateView.as_view(),  name='create'),
    path('<int:pk>/',          views.TaskDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/',     views.TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/',   views.TaskDeleteView.as_view(), name='delete'),
]
