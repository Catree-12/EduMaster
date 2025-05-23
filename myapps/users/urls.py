from django.urls import path
from .views import User_register, User_login
urlpatterns = [
    path('register/', User_register.as_view(), name='register'),
    path('login/', User_login.as_view(), name='login'),
]