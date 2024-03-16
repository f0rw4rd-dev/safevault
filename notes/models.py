from django.db import models
from django.utils import timezone


class Note(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='note_records')
    title = models.CharField(max_length=480)
    data = models.CharField(max_length=40960)
    init_vector = models.CharField(max_length=160)
    status = models.PositiveIntegerField(default=0)
    change_status_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
