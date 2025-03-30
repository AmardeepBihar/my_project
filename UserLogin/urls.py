from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register, name='user_register'),
    path('login/', views.Login, name='user_login'),
    path('logout/', views.Logout, name='user_logout'),
    path('profile/', views.Profile, name='user_profile'),
]