# Generated by Django 3.1.4 on 2021-01-26 20:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_viewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='viewers',
            field=models.ManyToManyField(related_name='read_posts', through='blog.UserPostRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]
