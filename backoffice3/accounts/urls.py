from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, check_email, UserListView, UserDetailView, StandbyUserListView, StandbyUserDetailView, update_permission, update_level, reject_user, approve_user

app_name = 'accountapp' 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('check-email/', check_email, name='check_email'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('standby/', StandbyUserListView.as_view(), name='standby_user_list'),
    path('standby/<int:pk>/', StandbyUserDetailView.as_view(), name='standby_user_detail'),
    path('standby/<int:pk>/update_permission/', update_permission, name='update_permission'),
    path('reject/<int:pk>/', reject_user, name='reject_user'),
    path('update_level/<int:pk>/', update_level, name='update_level'),
    path('approve_user/<int:pk>/', approve_user, name='approve_user'),
]
