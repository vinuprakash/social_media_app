from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    fields = [ 'username','email','first_name','last_name','password']

    search_fields = ['username']

    list_display = ['username','email','first_name','last_name']


admin.site.register(models.User,UserAdmin)
