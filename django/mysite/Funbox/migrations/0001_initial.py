# Generated by Django 4.0.3 on 2022-04-12 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.IntegerField(db_column='Group_id', primary_key=True, serialize=False)),
                ('group_name', models.CharField(blank=True, db_column='Group_name', max_length=45, null=True)),
            ],
            options={
                'db_table': 'group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('note_id', models.IntegerField(db_column='Note_id', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, db_column='Created_At', null=True)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'note',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.CharField(db_column='User_ID', max_length=45, primary_key=True, serialize=False)),
                ('password', models.CharField(db_column='Password', max_length=45)),
                ('user_email', models.CharField(db_column='User_Email', max_length=45)),
                ('user_name', models.CharField(blank=True, db_column='User_Name', max_length=45, null=True)),
            ],
            options={
                'db_table': 'user_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('activities_id', models.IntegerField(db_column='Activities_id', primary_key=True, serialize=False)),
                ('activity_desc', models.CharField(blank=True, db_column='Activity_desc', max_length=45, null=True)),
                ('activity_timelength', models.IntegerField(blank=True, db_column='Activity_timeLength', null=True)),
                ('activity_photo', models.ImageField(default='user1.jpg', upload_to='photos')),
            ],
            options={
                'db_table': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('user_info_commentor', models.OneToOneField(db_column='User_info_Commentor_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Funbox.userinfo')),
                ('createdat', models.DateTimeField(blank=True, db_column='CreatedAt', null=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('group_group', models.OneToOneField(db_column='Group_Group_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Funbox.group')),
                ('content', models.CharField(blank=True, db_column='Content', max_length=1000, null=True)),
                ('created_at', models.DateTimeField(blank=True, db_column='Created_At', null=True)),
            ],
            options={
                'db_table': 'group_message',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('user_info_sender', models.OneToOneField(db_column='User_info_Sender_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='Sender', serialize=False, to='Funbox.userinfo')),
                ('created_at', models.DateTimeField(blank=True, db_column='Created_At', null=True)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'message',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rankings',
            fields=[
                ('activities_activities', models.OneToOneField(db_column='Activities_Activities_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Funbox.activities')),
                ('ranking', models.IntegerField(blank=True, db_column='Ranking', null=True)),
                ('created_at', models.DateTimeField(blank=True, db_column='Created_At', null=True)),
            ],
            options={
                'db_table': 'rankings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('user_info_user', models.OneToOneField(db_column='User_info_User_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Funbox.userinfo')),
                ('created_at', models.DateTimeField(blank=True, db_column='Created_at', null=True)),
            ],
            options={
                'db_table': 'user_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfoHasGroup',
            fields=[
                ('user_info_user', models.OneToOneField(db_column='User_info_User_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Funbox.userinfo')),
            ],
            options={
                'db_table': 'user_info_has_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('user_info_user', models.OneToOneField(db_column='User_info_User_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='Funbox.userinfo')),
            ],
            options={
                'db_table': 'user_preference',
                'managed': False,
            },
        ),
    ]