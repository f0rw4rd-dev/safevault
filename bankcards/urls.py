from django.urls import path
from . import views

app_name = 'bankcards'
urlpatterns = [
    path('', views.BankcardsView.as_view(), name='bankcards'),
    path('api/update/status/', views.UpdateBankcardStatusView.as_view(), name='update_bankcard_status'),
    path('api/delete/', views.DeleteBankcardView.as_view(), name='delete_bankcard'),
]
