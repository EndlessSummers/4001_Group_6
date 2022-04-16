# Generated by Django 4.0.3 on 2022-04-16 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Funbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(default='', max_length=200, null=True)),
                ('activity', models.ForeignKey(default='Hiking', on_delete=django.db.models.deletion.CASCADE, to='Funbox.activities')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Funbox.userinfo')),
            ],
            options={
                'db_table': 'notes',
                'managed': True,
                'unique_together': {('user', 'activity')},
            },
        ),
    ]