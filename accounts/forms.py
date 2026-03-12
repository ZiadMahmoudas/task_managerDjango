"""
accounts/forms.py

Registration and authentication forms.
We extend Django's built-in forms to keep password hashing, validation,
and security in the framework's hands while adding Bootstrap styling.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Extends UserCreationForm to include an email field and Bootstrap styling.
    UserCreationForm already handles duplicate username checks and password
    confirmation validation — we don't need to rewrite that logic.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to all inherited fields
        for field_name in ('username', 'password1', 'password2'):
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

    def save(self, commit=True):
        """Save the email field alongside the inherited user fields."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Extends Django's AuthenticationForm to add Bootstrap styling.
    AuthenticationForm handles credential verification and brute-force
    protections internally — no need to reimplement.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
