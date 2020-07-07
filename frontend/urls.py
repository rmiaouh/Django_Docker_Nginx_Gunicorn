from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('', views.home, name="home"),
    path('home-p2/', views.home2, name="home2"),
    path('logout/', views.logoutUser, name="logout"),
]
