from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *

'''
admin.site.register(Post)
admin.site.register(Tag)
'''

@admin.register(Post)
class PostAdmin(ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass

@admin.register(UserPostRelation)
class UserPostRelationAdmin(ModelAdmin):
    pass
