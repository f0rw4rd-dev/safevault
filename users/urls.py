from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('reset/', views.ResetView.as_view(), name='reset'),
    path('reset-2/', views.Reset2View.as_view(), name='reset-2'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/', views.UserAPIView.as_view()),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
