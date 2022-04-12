# Generated by Django 4.0.3 on 2022-04-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Funbox', '0004_alter_activities_options_alter_userinfo_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user_photo',
            field=models.ImageField(blank=True, default='user1.jpg', upload_to='photos_user'),
        ),
        migrations.AlterField(
            model_name='activities',
            name='activity_photo',
            field=models.ImageField(blank=True, default='activity.jpg', upload_to='photos'),
        ),
    ]
