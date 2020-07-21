from django.urls import path
from . import views

urlpatterns = [
    path('babel/', views.list, name="list"),
    path('orange/', views.orangepage, name="orangepage"),
    path('pink/', views.pinkpage, name="pinkpage"),
    path('yellow/', views.yellowpage, name="yellowpage"),
    path('red/', views.redpage, name="redpage"),
    path('blue/', views.bluepage, name="bluepage"),
    path('green/', views.greenpage, name="greenpage"),
    path('ra/', views.rapage, name="rapage"),
    path('login/', views.loginPage, name="login"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('logout/', views.logoutUser, name="logout"),
]
