# Generated by Django 4.1.5 on 2023-02-02 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
