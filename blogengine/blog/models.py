from time import time
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from django.contrib.auth.models import User


def gen_slug(s):
    return f'{slugify(s, allow_unicode=True)}'


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    body = models.TextField(db_index=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modify_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    viewers = models.ManyToManyField(User, through='UserPostRelation', related_name='read_posts')

    class Meta:
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = f'{gen_slug(self.title)}-{int(time())}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserPostRelation(models.Model):
    RATE_CHOICES = (
        (1, 'meh'),
        (2, 'ok'),
        (3, 'fine'),
        (4, 'good'),
        (5, 'amazing')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user}, post: {self.post.title}, rated as {self.rate}'


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
