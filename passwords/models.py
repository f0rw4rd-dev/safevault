from django.db import models
from django.utils import timezone


class Password(models.Model):
    title = models.CharField(max_length=480, blank=False, null=False)
    website = models.CharField(max_length=2560)
    login = models.CharField(max_length=1280)
    email = models.CharField(max_length=1280)
    password = models.CharField(max_length=1280, blank=False, null=False)
    extra_data = models.CharField(max_length=40960)
    init_vector = models.CharField(max_length=160, blank=False, null=False)
    status = models.PositiveIntegerField(default=0, blank=False, null=False)
    change_status_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
