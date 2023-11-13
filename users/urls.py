from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('Register/', views.Register, name='Register'),
    path('change-password/', views.change_password, name='change_password'),
]