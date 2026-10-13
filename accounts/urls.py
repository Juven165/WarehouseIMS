from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('send-activation-email/', views.send_verification_email, name='send_activation_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.send_password_reset_email, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('my-profile/', views.my_profile, name='my_profile'),
]