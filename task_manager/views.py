from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View

from django.http import HttpResponse


def error_404(request, exception):
    return render(request, '404.html')


class IndexView(View):
    """Root index view for Anonumus and Logged user."""
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class CustomLoginView(SuccessMessageMixin, LoginView):
    """User login page view."""
    template_name = 'user/login.html'
    next_page = reverse_lazy('home')
    success_message = _("You are logged in")


class CustomLogoutView(LogoutView):
    """Integrate message in get_next_page."""
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        msg_text = _("You are logged out")
        messages.info(self.request, msg_text)
        return response
