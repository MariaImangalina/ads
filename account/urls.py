from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SignUp


app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/'), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
]