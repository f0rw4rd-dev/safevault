# Generated by Django 5.0.3 on 2024-03-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankcards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankcard',
            name='card_pin',
            field=models.CharField(default=0, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bankcard',
            name='init_vector',
            field=models.CharField(default=0, max_length=160),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankcard',
            name='card_expiration_month',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='bankcard',
            name='card_expiration_year',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='bankcard',
            name='card_security_code',
            field=models.CharField(max_length=60),
        ),
    ]