from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.NotesView.as_view(), name='notes'),
    path('api/update/status/', views.UpdateNoteStatusView.as_view(), name='update_note_status'),
    path('api/delete/', views.DeleteNoteView.as_view(), name='delete_note'),
]
