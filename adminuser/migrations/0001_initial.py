# Generated by Django 5.0 on 2024-01-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Package_name', models.CharField(max_length=255)),
                ('Package_fee', models.IntegerField()),
                ('Package_duration', models.IntegerField()),
                ('Package_description', models.TextField()),
            ],
        ),
    ]
