# Generated by Django 4.0.3 on 2022-04-16 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Funbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userhash',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='userhash',
            table='user_hash',
        ),
    ]
