# Generated by Django 5.0 on 2024-01-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_message_request_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_request',
            name='is_notify',
            field=models.BooleanField(default=False),
        ),
    ]
