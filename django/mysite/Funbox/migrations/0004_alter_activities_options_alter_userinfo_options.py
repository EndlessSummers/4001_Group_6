# Generated by Django 4.0.3 on 2022-04-12 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Funbox', '0003_remove_activity_activity_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activities',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'managed': True},
        ),
    ]