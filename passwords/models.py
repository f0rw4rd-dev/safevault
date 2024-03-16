from django.db import models
from django.utils import timezone


class Password(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='password_records')
    title = models.CharField(max_length=480)
    website = models.CharField(max_length=2560, blank=True, null=True)
    login = models.CharField(max_length=1280)
    email = models.CharField(max_length=1280, blank=True, null=True)
    password = models.CharField(max_length=1280)
    extra_data = models.CharField(max_length=40960, blank=True, null=True)
    init_vector = models.CharField(max_length=160)
    status = models.PositiveIntegerField(default=0)
    change_status_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
