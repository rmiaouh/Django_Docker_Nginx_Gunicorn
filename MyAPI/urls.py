from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('task-babel/', views.taskCreate, name="task-create"),
    path('task-orange/', views.taskCreate_orange, name="task-create-orange"),
    path('task-yellow/', views.taskCreate_yellow, name="task-create-yellow"),


    path('task-list/', views.taskList, name="task-list"),
    path('task-list-orange/', views.taskList_orange, name="task-list-orange"),
    path('task-list-yellow/', views.taskList_yellow, name="task-list-yellow"),




    path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
    path('task-delete-orange/<str:pk>/', views.taskDeleteOrange, name="task-delete-orange"),
    path('task-delete-red/<str:pk>/', views.taskDeleteRed, name="task-delete-red"),
    path('task-delete-yellow/<str:pk>/', views.taskDeleteYellow, name="task-delete-yellow"),
    path('task-delete-pink/<str:pk>/', views.taskDeletePink, name="task-delete-pink"),
    path('task-delete-blue/<str:pk>/', views.taskDeleteBlue, name="task-delete-blue"),
    path('task-delete-green/<str:pk>/', views.taskDeleteGreen, name="task-delete-green"),


]