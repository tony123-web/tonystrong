from multiprocessing.resource_tracker import register
from tkinter.font import names

from .import  views
from django.urls import path

urlpatterns = [
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpape, name="logout"),
    path('register/', views.registerpage, name="register"),
    path('', views.home, name="home"),
    path('user_profile/<str:pk>/', views.userProfile, name="user_profile"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/',views.createRoom, name="create-room" ),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('update_user/', views.updateuser, name="update_user"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('all-topics/', views.topics_half_screen, name="all-topics"),
    path('activities/', views.activities_half_screen, name="activities"),

]
