# Generated by Django 4.1.5 on 2023-01-08 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0007_alter_mixins_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mixins',
            name='phone',
        ),
    ]
