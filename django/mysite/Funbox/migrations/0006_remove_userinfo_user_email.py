# Generated by Django 4.0.3 on 2022-04-14 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Funbox', '0005_userinfo_user_photo_alter_activities_activity_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='user_email',
        ),
    ]