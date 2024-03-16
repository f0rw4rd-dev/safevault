from django.db import models
from django.utils import timezone


class Bankcard(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bankcard_records')
    title = models.CharField(max_length=480)
    card_number = models.CharField(max_length=160)
    card_expiration_month = models.CharField(max_length=20)
    card_expiration_year = models.CharField(max_length=40)
    card_security_code = models.CharField(max_length=30)
    cardholder_name = models.CharField(max_length=1280, blank=True, null=True)
    extra_data = models.CharField(max_length=40960, blank=True, null=True)
    status = models.PositiveIntegerField(default=0)
    change_status_time = models.DateTimeField(default=timezone.now)
