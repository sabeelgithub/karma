# Generated by Django 4.1.5 on 2023-02-03 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_return_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
