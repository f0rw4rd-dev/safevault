from django.db import models
from django.utils import timezone


class Address(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='address_records')
    title = models.CharField(max_length=480)
    country = models.CharField(max_length=1280)
    region = models.CharField(max_length=1280, blank=True, null=True)
    locality = models.CharField(max_length=1280)
    street = models.CharField(max_length=1280)
    house = models.CharField(max_length=160)
    zip_code = models.CharField(max_length=160)
    extra_data = models.CharField(max_length=40960, blank=True, null=True)
    init_vector = models.CharField(max_length=160)
    status = models.PositiveIntegerField(default=0)
    change_status_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
