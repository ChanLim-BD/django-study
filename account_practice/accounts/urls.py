from django.urls import path

from .views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signin/', SignInView.as_view()),
    path('signout/', SignOutView.as_view()),
]