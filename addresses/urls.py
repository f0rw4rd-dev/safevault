from django.urls import path
from . import views

app_name = 'addresses'
urlpatterns = [
    path('', views.AddressesView.as_view(), name='addresses'),
    path('api/update/status/', views.UpdateAddressStatusView.as_view(), name='update_address_status'),
    path('api/delete/', views.DeleteAddressView.as_view(), name='delete_address'),
]
