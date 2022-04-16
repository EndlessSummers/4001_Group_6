# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Model
#from django.contrib.postgres.fields import ArrayField 


class Activities(models.Model):
    activities_id = models.CharField(db_column='Activities_id', max_length = 45, primary_key=True)  # Field name made lowercase.
    activity_desc = models.CharField(db_column='Activity_desc', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    activity_timelength = models.IntegerField(db_column='Activity_timeLength', blank=True, null=True)  # Field name made lowercase.
    activity_photo = models.ImageField(blank = True, upload_to='photos_activities', default='activity.jpg')
    activity_participant = models.IntegerField(blank = True, null = False, default = 1)
    activity_place = models.CharField(blank =True, max_length = 25, default = "Home")
    activity_tag = models.CharField(blank = True, max_length = 20, default = "Game")
    class Meta:
        managed = True
        db_table = 'activities'


class UserInfo(models.Model):
    user_id = models.CharField(db_column='User_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=45)  # Field name made lowercase.
    #user_email = models.CharField(db_column='User_Email', max_length=45)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_Name', max_length=20, blank=True, null=True, default="null")  # Field name made lowercase.
    user_photo = models.ImageField(blank = True, upload_to='photos_user/', default='photos_user/Nick_Wilde.jpg')

    class Meta:
        managed = True
        db_table = 'user_info'


class UserPreference(models.Model):
    user = models.ForeignKey(UserInfo, models.CASCADE)  # Field name made lowercase.
    activity = models.ForeignKey(Activities, models.CASCADE, default = "Hiking")  # Field name made lowercase.
    likes = models.BooleanField(default = False)

    class Meta:
        managed = True
        db_table = 'user_preference'
        unique_together = (('user', 'activity'),)

class Notes(models.Model):
    user = models.ForeignKey(UserInfo, models.CASCADE)  # Field name made lowercase.
    activity = models.ForeignKey(Activities, models.CASCADE, default = "Hiking")  # Field name made lowercase.
    title = models.CharField(max_length = 50, default = "", null = True)
    note = models.CharField(max_length = 500, default = "", null = True)
    activity_photo = models.ImageField(blank = True, upload_to='photos_notes', default='notes.jpg')

    class Meta:
        managed = True
        db_table = 'notes'


class UserHash(models.Model):
    user_id = models.CharField(db_column='User_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    hashnum = models.CharField(db_column='Password', max_length=1000, default = "")  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'user_hash'

class notelikes(models.Model):
    user = models.ForeignKey(UserInfo, models.CASCADE)  # Field name made lowercase.
    note = models.ForeignKey(Notes, models.CASCADE)  # Field name made lowercase.
    likes = models.BooleanField(default = False)

    class Meta:
        managed = True
        unique_together = (('user', 'note'),)
