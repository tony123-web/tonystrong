from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('logout/', views.user_logout, name="logout"),
    path('login/', views.user_login, name="login"),
    path('register/', views.registration, name="register"),
    path('email/', views.user_email_activation_link, name="email"),
    path('activate/<uidb64>/<token>/', views.activation, name="activate"),
    path('reset-password/', views.reset_password, name="reset-password"),
    path('reset-password-confirm/<uidb64>/<token>/ ', views.reset_password_confirm,
         name='reset-password-confirm'),
]
