"""
accounts/views.py

Handles user registration and login.
Password reset is handled entirely by Django's built-in views (wired in urls.py).
Logout uses Django's built-in LogoutView.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    """
    Handles GET (show form) and POST (process registration).

    After successful registration, logs the user in automatically
    and redirects to their task dashboard for a smooth onboarding experience.
    """

    template_name = 'accounts/register.html'

    def get(self, request):
        # If already authenticated, redirect away from register page
        if request.user.is_authenticated:
            return redirect('tasks:dashboard')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('tasks:dashboard')
        # Form is invalid — re-render with validation errors
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    """
    Extends Django's LoginView to use our custom styled form
    and redirect authenticated users away from the login page.
    """

    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tasks:dashboard')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)
