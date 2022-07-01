
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import LoginForm
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(
        form_class=LoginForm,
        template_name='accounts/login_form.html'
        ), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]