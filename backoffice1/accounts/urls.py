from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, check_email, SignInView, StandbyUserListView, StandbyUserDetailView, StandbyUserPromoteView

app_name = 'accounts' 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('check-email/', check_email, name='check_email'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'), 
    path('users-standby/', StandbyUserListView.as_view(), name='standby_user_list'),
    path('users-standby/<int:pk>/', StandbyUserDetailView.as_view(), name='standby_user_detail'),
    path('users-standby/<int:pk>/promote/', StandbyUserPromoteView.as_view(), name='standby_user_promote'),
    
]
