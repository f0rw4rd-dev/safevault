from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils import timezone

from .managers import UserManager

import datetime


class User(AbstractBaseUser):
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False)
    auth_key = models.CharField(max_length=2560, blank=False, null=False)
    salt = models.CharField(max_length=160, blank=False, null=False)
    init_vector = models.CharField(max_length=160, blank=False, null=False)
    tfa_key = models.CharField(max_length=160, blank=True, null=True)
    session_duration = models.PositiveIntegerField(default=30, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    auth_attempts = models.PositiveIntegerField(default=3, blank=False, null=False)
    auth_last_attempt_time = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0, 0, datetime.timezone.utc), blank=False, null=False)
    auth_lock_end_time = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0, 0, datetime.timezone.utc), blank=False, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['auth_key', 'salt', 'init_vector']

    def __str__(self):
        return self.email


def default_reset_end_time():
    return timezone.now() + datetime.timedelta(hours=1)


class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_key = models.CharField(max_length=64, blank=False, null=False)
    reset_end_time = models.DateTimeField(default=default_reset_end_time, blank=False, null=False)
