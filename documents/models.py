from django.db import models
from django.utils import timezone


class Document(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='document_records')
    title = models.CharField(max_length=480)
    document_number = models.CharField(max_length=320)
    issuing_authority = models.CharField(max_length=2560, blank=True, null=True)
    issue_date = models.CharField(max_length=160, blank=True, null=True)
    expiration_date = models.CharField(max_length=160, blank=True, null=True)
    extra_data = models.CharField(max_length=40960, blank=True, null=True)
    init_vector = models.CharField(max_length=160)
    status = models.PositiveIntegerField(default=0)
    change_status_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
