"""
dashboard/mixins.py

StaffRequiredMixin is our access control gate for all admin dashboard views.

How it works:
1. LoginRequiredMixin ensures the user is authenticated.
2. UserPassesTestMixin runs test_func() — if it returns False, the user
   gets a 403 Forbidden response instead of the admin page.

Why not just check is_staff in each view?
- DRY principle: one place to change the policy.
- Easy to audit: grep for StaffRequiredMixin to find all protected views.
- Composable: can be combined with other mixins.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Restricts access to staff members (is_staff=True) or superusers.
    Raises a 403 for authenticated non-staff users.
    Redirects unauthenticated users to the login page.
    """

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
