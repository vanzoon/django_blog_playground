from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class RegularUsers(Group):
    name = 'Regular users'
    permissions = (
       'blog.add_post', 'blog.update_post',
       'blog.delete_post', 'blog.view_post',
       'users.add_user', 'users.update_user',
       'users.delete_user', 'users.view_user',
        )


class User(AbstractUser):
    age = models.PositiveIntegerField(default=None, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            instance.groups.add(
                Group.objects.get(name='Regular users'))

    def __str__(self):
        return self.username
