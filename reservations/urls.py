from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_register/', views.login_register, name='login_register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('profile/', views.profile, name='profile'),
    path('edit_reservation/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:pk>/', views.delete_reservation, name='delete_reservation'),
]
