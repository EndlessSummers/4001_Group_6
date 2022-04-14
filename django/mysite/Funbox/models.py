# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Model

class Activity(models.Model):
    activities_id = models.IntegerField(db_column='Activity_id', primary_key=True)  # Field name made lowercase.
    activity_desc = models.CharField(db_column='Activity_desc', max_length=45, blank=True, null=True)  # Field name made lowercase.
    activity_timelength = models.IntegerField(db_column='Activity_timeLength', blank=True, null=True)  # Field name made lowercase.
    #activity_photo = models.ImageField(upload_to='photos', default='user1.jpg')
    class Meta:
        db_table = 'activity'

class Activities(models.Model):
    activities_id = models.IntegerField(db_column='Activities_id', primary_key=True)  # Field name made lowercase.
    activity_desc = models.CharField(db_column='Activity_desc', max_length=45, blank=True, null=True)  # Field name made lowercase.
    activity_timelength = models.IntegerField(db_column='Activity_timeLength', blank=True, null=True)  # Field name made lowercase.
    activity_photo = models.ImageField(blank = True, upload_to='photos', default='activity.jpg')
    class Meta:
        managed = True
        db_table = 'activities'


class Comment(models.Model):
    user_info_commentor = models.OneToOneField('UserInfo', models.DO_NOTHING, db_column='User_info_Commentor_ID', primary_key=True)  # Field name made lowercase.
    note_note = models.ForeignKey('Note', models.DO_NOTHING, db_column='Note_Note_id')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'comment'
        unique_together = (('user_info_commentor', 'note_note'),)


class Group(models.Model):
    group_id = models.IntegerField(db_column='Group_id', primary_key=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='Group_name', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group'


class GroupMessage(models.Model):
    group_group = models.OneToOneField(Group, models.DO_NOTHING, db_column='Group_Group_id', primary_key=True)  # Field name made lowercase.
    user_info_user = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='User_info_User_ID')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_At', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'group_message'
        unique_together = (('group_group', 'user_info_user'),)


class Message(models.Model):
    user_info_sender = models.OneToOneField('UserInfo', models.DO_NOTHING, db_column='User_info_Sender_ID', primary_key=True, related_name='Sender')  # Field name made lowercase.
    user_info_receiver_id = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='User_info_Receiver_ID',related_name='Receiver')  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_At', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'message'
        unique_together = (('user_info_sender', 'user_info_receiver_id'),)


class Note(models.Model):
    note_id = models.IntegerField(db_column='Note_id', primary_key=True)  # Field name made lowercase.
    user_info_user = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='User_info_User_ID')  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_At', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'note'


class Rankings(models.Model):
    activities_activities = models.OneToOneField(Activities, models.DO_NOTHING, db_column='Activities_Activities_id', primary_key=True)  # Field name made lowercase.
    user_info_user = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='User_info_User_ID')  # Field name made lowercase.
    ranking = models.IntegerField(db_column='Ranking', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_At', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'rankings'
        unique_together = (('activities_activities', 'user_info_user'),)


class UserHistory(models.Model):
    user_info_user = models.OneToOneField('UserInfo', models.DO_NOTHING, db_column='User_info_User_ID', primary_key=True)  # Field name made lowercase.
    activities_activities = models.ForeignKey(Activities, models.DO_NOTHING, db_column='Activities_Activities_id')  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_at', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'user_history'
        unique_together = (('user_info_user', 'activities_activities'),)


class UserInfo(models.Model):
    user_id = models.CharField(db_column='User_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=45)  # Field name made lowercase.
    user_email = models.CharField(db_column='User_Email', max_length=45)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    user_photo = models.ImageField(blank = True, upload_to='photos_user', default='user1.jpg')

    class Meta:
        managed = True
        db_table = 'user_info'


class UserInfoHasGroup(models.Model):
    user_info_user = models.OneToOneField(UserInfo, models.DO_NOTHING, db_column='User_info_User_ID', primary_key=True)  # Field name made lowercase.
    group_group = models.ForeignKey(Group, models.DO_NOTHING, db_column='Group_Group_id')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'user_info_has_group'
        unique_together = (('user_info_user', 'group_group'),)


class UserPreference(models.Model):
    user_info_user = models.OneToOneField(UserInfo, models.DO_NOTHING, db_column='User_info_User_ID', primary_key=True)  # Field name made lowercase.
    activities_activities = models.ForeignKey(Activities, models.DO_NOTHING, db_column='Activities_Activities_id')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'user_preference'
        unique_together = (('user_info_user', 'activities_activities'),)

