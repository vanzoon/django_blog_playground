from time import time
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User

from blogengine import settings

# TODO: pay attention to slug and cyrillic


def gen_slug(s):
    return f'{slugify(s, allow_unicode=True)}'


class PostQuerySet(models.QuerySet):

    def get_queryset(self):
        return super().select_related('author').prefetch_related('tags')

    def filter_author_admin(self):
        return self.filter(author='admin')

    def order_by_rating_and_viewers(self):
        args = ('rating', 'viewers')
        return self.order_by(*args)
    
    def search(self, search_query):
        return self.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        ).select_related('author').prefetch_related('tags')


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def filter_author_admin(self):
        return self.get_queryset().filter_author_admin()

    def order_by_rating_and_viewers(self):
        return self.get_queryset().order_by_rating_and_viewers()

    def search(self, search_query):
        return self.get_queryset().search(search_query)


class CommentManager(models.Manager):

    def comments_for_post(self, post):
        return super(CommentManager, self).filter(post=post, active=True)


class Post(models.Model):
    STATUS = (
        (0, 'Draft'),
        (1, 'Published')
    )

    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    body = models.TextField(db_index=True, verbose_name='Contents', blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modify_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    viewers = models.ManyToManyField(User, through='UserPostRelation', related_name='read_posts')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True, blank=True)

    objects = PostManager()

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
        else:
            self.last_modify_date = timezone.now()
        # self.author = self.request.user
        super().save(*args, **kwargs)

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

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
        return f'{self.user}, post: {self.post}, rated as {self.rate}'

    def __init__(self, *args, **kwargs):
        super(UserPostRelation, self).__init__(*args, **kwargs)
        self.__old_rate = self.rate

    def save(self, *args, **kwargs):
        creating = not self.pk
        super(UserPostRelation, self).save(*args, **kwargs)
        if self.__old_rate != self.rate or creating:
            from api.logic import set_rating
            set_rating(self.post)
            self.__old_rate = self.rate


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f"Comment by {self.name}: {self.body}"


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
        if not self.pk:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
