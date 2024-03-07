from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib import messages
from django.utils.translation import gettext as _


class UserLimitChangeMixin(UserPassesTestMixin):
    """Limit the user ability to change other users."""

    def test_func(self):
        """Check if the user ID match with ID extracted from URL parameters."""
        user_id = self.kwargs.get('pk')
        return self.request.user.pk == user_id

    def handle_no_permission(self):
        """Redirect to users index with flash msg."""
        msg_text = _("You don't have permition to change other user")
        messages.error(self.request, msg_text)
        return redirect('users_index')
