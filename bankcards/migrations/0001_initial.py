# Generated by Django 5.0.3 on 2024-03-16 07:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bankcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=480)),
                ('card_number', models.CharField(max_length=160)),
                ('card_expiration_month', models.CharField(max_length=20)),
                ('card_expiration_year', models.CharField(max_length=40)),
                ('card_security_code', models.CharField(max_length=30)),
                ('cardholder_name', models.CharField(blank=True, max_length=1280, null=True)),
                ('extra_data', models.CharField(blank=True, max_length=40960, null=True)),
                ('status', models.PositiveIntegerField(default=0)),
                ('change_status_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bankcard_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
