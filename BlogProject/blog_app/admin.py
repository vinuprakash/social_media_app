from django.contrib import admin
from . import models

# Register your models here.

class PostAdmin(admin.ModelAdmin):

    search_fields = ['title']

    list_display = ['title','author']

class CommentAdmin(admin.ModelAdmin):

    fields = ['author','post','content']

    list_display = ['post', 'author']

class LikeAdmin(admin.ModelAdmin):

    fields = ['post','user']
    list_display = ['post.title','user.username']

admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Like)
