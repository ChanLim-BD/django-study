from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, check_email, StandbyUserListView, StandbyUserDetailView

app_name = 'accountapp' 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('check-email/', check_email, name='check_email'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users-standby/', StandbyUserListView.as_view(), name='standby_user_list'),
    path('users-standby/<int:pk>/', StandbyUserDetailView.as_view(), name='standby_user_detail'),  
]
