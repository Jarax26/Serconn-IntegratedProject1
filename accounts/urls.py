from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path('user/<int:user_id>/', views.user_profile_view, name='user_profile'),
]