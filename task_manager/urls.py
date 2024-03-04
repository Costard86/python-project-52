from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('users/', include('task_manager.user.urls')),
    path(
        'login/',
        views.CustomLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.CustomLogoutView.as_view(),
        name='logout'
    ),
    path('statuses/', include('task_manager.status.urls')),
    path('tasks/', include('task_manager.task.urls')),
    path('labels/', include('task_manager.label.urls')),
    path('admin/', admin.site.urls),
]
