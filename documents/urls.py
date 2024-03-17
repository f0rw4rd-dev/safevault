from django.urls import path
from . import views

app_name = 'documents'
urlpatterns = [
    path('', views.DocumentsView.as_view(), name='documents'),
    path('api/update/status/', views.UpdateDocumentStatusView.as_view(), name='update_document_status'),
    path('api/delete/', views.DeleteDocumentView.as_view(), name='delete_document'),
]
