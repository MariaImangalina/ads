from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SignUp, UserDetail, UserList, check_payment


app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/'), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('user/<int:pk>/', UserDetail.as_view(), name='userpage'),
    path('all/', UserList.as_view(), name='all'),
    path('check_payment/', check_payment, name='check_payment'),
]