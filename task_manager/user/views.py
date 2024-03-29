from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from . import forms
from .mixins import UserLimitChangeMixin


class UsersView(View):
    """Users page view."""

    def get(self, request, *args, **kwargs):
        """Return all users."""
        users = User.objects.all()
        return render(request, 'user/index.html', {'users': users})


class UserCreateView(View):
    """User create page view."""

    def get(self, request, *args, **kwargs):
        """Return a user creation form."""
        form = forms.CustomUserCreationForm()
        return render(request, 'user/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Create a new user."""
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            msg_text = _('User is successfully created')
            messages.success(request, msg_text)
            return redirect('login')
        return render(request, 'user/create.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, UserLimitChangeMixin, UpdateView):
    """User update page view."""
    login_url = reverse_lazy('login')
    template = 'user/update.html'

    def get(self, request, *args, **kwargs):
        """Return a user data filled form."""
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        form = forms.CustomUserChangeForm(instance=user)
        return render(
            request,
            self.template,
            {'form': form, 'user_id': user_id}
        )

    def post(self, request, *args, **kwargs):
        """Update a user data."""
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        form = forms.CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            msg_text = _('User is successfully updated')
            messages.success(request, msg_text)
            return redirect('users_index')
        return render(
            request,
            self.template,
            {'form': form, 'user_id': user_id}
        )


class UserDeleteView(LoginRequiredMixin, UserLimitChangeMixin, View):
    """User delete page view."""
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        """Render delete user template."""
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        return render(request, 'user/delete.html', {'user': user})

    def post(self, request, *args, **kwargs):
        """Delete user."""
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        user.delete()
        msg_text = _('User is successfully deleted')
        messages.success(request, msg_text)
        return redirect('users_index')
