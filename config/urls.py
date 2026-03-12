"""
Root URL configuration for Task Manager.

URL namespaces are used throughout to prevent naming collisions
and enable {% url 'app:view_name' %} in templates.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Django built-in admin panel
    path('admin/', admin.site.urls),

    # Redirect root URL to the login page
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),

    # accounts app: login, register, logout, password reset
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # tasks app: user-facing task CRUD and dashboard
    path('tasks/', include('tasks.urls', namespace='tasks')),

    # dashboard app: admin-only statistics and management views
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
