from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Authentication paths
    path('logout/', views.logout, name='logout'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), #
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name ='login'),
    path('register/', views.register, name='register'),
    path('login_pass_update/', views.login_pass_update, name='login_pass_update'),
    path('update_password/', views.update_password, name='update_password'),
    # path('update_profile_password/', views.update_profile_password, name='update_profile_password'),

    # Student profile and image paths
    path('profile/<int:student_id>/', views.profile, name='profile'),
    path('student_image/<int:student_id>/', views.student_image, name='student_image'),
    path('update_std_photo/', views.update_std_photo, name='update_std_photo'),

    # Student biometric data and other updates
    path('std_update_bio/', views.std_update_bio, name='std_update_bio'),

    
]
