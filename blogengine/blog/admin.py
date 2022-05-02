from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # list_display = all


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
    pass

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    search_fields = ('name', 'email', 'body')
    list_filter = ('active', 'pub_date')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
