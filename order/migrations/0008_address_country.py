# Generated by Django 4.1.5 on 2023-02-02 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
