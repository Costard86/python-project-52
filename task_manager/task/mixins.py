from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Task


class UserLimitDeleteMixin(UserPassesTestMixin):
    """Limit the user ability to delete only his own tasks."""

    def test_func(self):
        """Check if the user ID match with ID extracted from URL parameters."""
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return self.request.user.pk == task.author_id

    def handle_no_permission(self):
        """Redirect to users index with flash msg."""
        msg_text = _("You don't have permition to delete the task")
        messages.error(self.request, msg_text)
        return redirect('tasks_index')
