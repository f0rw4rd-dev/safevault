# Generated by Django 5.0.3 on 2024-03-14 12:56

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
            name='Password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=480)),
                ('website', models.CharField(max_length=2560)),
                ('login', models.CharField(max_length=1280)),
                ('email', models.CharField(max_length=1280)),
                ('password', models.CharField(max_length=1280)),
                ('extra_data', models.CharField(max_length=40960)),
                ('init_vector', models.CharField(max_length=160)),
                ('status', models.PositiveIntegerField(default=0)),
                ('change_status_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
