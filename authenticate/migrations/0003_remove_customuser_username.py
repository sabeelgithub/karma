# Generated by Django 4.1.5 on 2023-01-06 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0002_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
