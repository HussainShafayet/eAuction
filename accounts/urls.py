from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/',views.ResetPassword.as_view(), name='password_reset'),
    path('password_reset/done/',views.ResetPasswordDone.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',views.ResetPasswordConfirm.as_view(),name='password_reset_confirm'),
    path('reset/done/', views.ResetPasswordComplete.as_view(),name='password_reset_complete'),
]
