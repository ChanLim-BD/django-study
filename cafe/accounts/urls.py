from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', SignOutView.as_view(), name='signout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)