"""
dashboard/urls.py

Admin dashboard URL patterns.
All views are protected by StaffRequiredMixin.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',       views.AdminDashboardView.as_view(),  name='overview'),
    path('users/', views.AdminUserListView.as_view(),   name='users'),
    path('tasks/', views.AdminTaskListView.as_view(),   name='tasks'),
]
