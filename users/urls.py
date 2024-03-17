from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('reset/', views.ResetView.as_view(), name='reset'),
    path('reset/confirm/<str:reset_key>/', views.ResetConfirmView.as_view(), name='reset-confirm'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/', views.UserAPIView.as_view()),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
