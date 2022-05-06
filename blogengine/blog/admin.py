from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


@admin.register(Post)
class PostAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass


@admin.register(UserPostRelation)
class UserPostRelationAdmin(ModelAdmin):
    fields = ['user', 'post', 'like', 'in_bookmarks', 'rate']
    list_filter = ['user']


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    search_fields = ('name', 'email', 'body')
    list_filter = ('active', 'pub_date')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
