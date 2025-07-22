from django import contrib
from django.contrib import admin
from django.contrib.auth import models
#from account.models import Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Database_user
class AccountInline(admin.StackedInline):
# Register your models here.
    model=Database_user
    can_delete=False
    #verbose_name_plural="Database_users"

class CustomizedUserAdmin(UserAdmin):
    inlines=(AccountInline,)

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)


