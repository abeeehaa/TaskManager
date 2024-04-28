from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# from userauths.views import RegisterView
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(template_name="login.html"), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('signup/', views.signup, name='signup'),
]