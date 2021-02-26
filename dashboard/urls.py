from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import DashboardView


urlpatterns = [
    path('', login_required(DashboardView.as_view()), name='dashboard'),
]