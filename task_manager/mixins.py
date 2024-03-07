from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext as _


class NeedPermitMixin(UserPassesTestMixin):
    """Limit the user ability to change other users."""

    def test_func(self, obj_id):
        """Check if the user ID match with the given ID."""
        return self.request.user.pk == obj_id

    def handle_no_permission(self, msg_denied, redirect_way):
        """Redirect to tasks index with flash msg."""
        msg_text = _(msg_denied)
        messages.error(self.request, msg_text)
        return redirect(redirect_way)

    # def handle_no_permission(self):
    #     """Redirect to tasks index with flash msg."""
    #     msg_text = _("You don't have permission to delete the task")
    #     messages.error(self.request, msg_text)
    #     return redirect('tasks_index')
