from django.contrib import admin
from .models import Activities, UserInfo

admin.site.register(Activities)
admin.site.register(UserInfo)

class UAdmin(admin.ModelAdmin):
    dics = ('user_photo', 'activity_photo')

# Register your models here.
