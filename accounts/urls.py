from django.urls import path, re_path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView, name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
]
