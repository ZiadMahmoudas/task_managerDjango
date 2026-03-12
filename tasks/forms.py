"""
tasks/forms.py

Single TaskForm used for both task creation and editing.
We explicitly define widgets to ensure Bootstrap 5 classes are applied,
and we exclude the 'user' field since it is set programmatically in the view.
"""

from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        # 'user' is excluded — it is assigned in the view from request.user
        # 'created_at' and 'updated_at' are auto-managed by the model
        fields = ('title', 'description', 'status', 'priority', 'due_date')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional description...',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',       # Renders as HTML5 date picker
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make description and due_date clearly optional in the UI
        self.fields['description'].required = False
        self.fields['due_date'].required = False


class TaskFilterForm(forms.Form):
    """
    A non-model form used to render the search/filter bar on the task list page.
    Validation here is simple — we use GET parameters, not saving any data.
    """

    EMPTY_CHOICE = [('', 'All')]

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tasks...',
        })
    )

    status = forms.ChoiceField(
        required=False,
        choices=EMPTY_CHOICE + Task.Status.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    priority = forms.ChoiceField(
        required=False,
        choices=EMPTY_CHOICE + Task.Priority.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
