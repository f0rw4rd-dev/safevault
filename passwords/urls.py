from django.urls import path
from . import views

app_name = 'passwords'
urlpatterns = [
    path('', views.PasswordsView.as_view(), name='passwords'),
    path('api/update/status/', views.UpdatePasswordStatusView.as_view(), name='update_password_status'),
    path('api/delete/', views.DeletePasswordView.as_view(), name='delete_password'),
    path('generator/', views.GeneratorView.as_view(), name='generator')
]
