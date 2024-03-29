from django.urls import path

from .views import SignUpView, SignInView, SignOutView, home

urlpatterns = [
    path('', home),
    path('signup', SignUpView.as_view()),
    path('signin', SignInView.as_view()),
    path('signout', SignOutView.as_view()),
]