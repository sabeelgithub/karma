# Generated by Django 4.1.5 on 2023-02-12 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_userprofile_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='wallet',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]