from django.urls import path

from . import views

app_name = 'passwords'
urlpatterns = [
    path('', views.PasswordsView.as_view(), name='passwords')
]
