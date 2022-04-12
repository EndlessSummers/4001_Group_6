# Generated by Django 4.0.3 on 2022-04-12 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Funbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activities_id', models.IntegerField(db_column='Activity_id', primary_key=True, serialize=False)),
                ('activity_desc', models.CharField(blank=True, db_column='Activity_desc', max_length=45, null=True)),
                ('activity_timelength', models.IntegerField(blank=True, db_column='Activity_timeLength', null=True)),
                ('activity_photo', models.ImageField(default='user1.jpg', upload_to='photos')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.AlterModelOptions(
            name='activities',
            options={'managed': False},
        ),
    ]
