# Generated by Django 4.1.5 on 2023-02-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_userprofile_address_line_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wallet',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
