# Generated by Django 4.1.5 on 2023-01-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0005_mixins_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mixins',
            name='phone',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
