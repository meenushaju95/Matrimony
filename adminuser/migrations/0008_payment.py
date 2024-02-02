# Generated by Django 5.0 on 2024-01-20 05:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminuser', '0007_image_remove_usermember_image_usermember_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_method', models.CharField(max_length=50)),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminuser.packages')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminuser.usermember')),
            ],
        ),
    ]