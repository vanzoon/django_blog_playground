from time import time
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify

from blogengine import settings

# TODO: pay attention to slug and cyrillic


def gen_slug(s):
    return f'{slugify(s, allow_unicode=True)}'


class PostQuerySet(models.QuerySet):

    def get_queryset(self):
        return super().select_related('author').prefetch_related('tags')

    # def get_detailed_queryset(self):
    #    return self.get_queryset().annotate(
    #        likes=Count(Case(When(userpostrelation__like=True, then=1)))
    #    )

    def get_published(self):
        return super().filter(status=1)

    def filter_author_admin(self):
        return self.filter(author__username='admin')

    def order_by_rating_and_viewers(self):
        args = ('rating', 'viewers')
        return self.order_by(*args)

    def search(self, search_query):
        return self.filter(
            Q(title__icontains=search_query) |
            Q(body__icontains=search_query)
        ).select_related('author')


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_published(self):
        return self.get_queryset().get_published()

    def filter_author_admin(self):
        return self.get_queryset().filter_author_admin()

    def order_by_rating_and_viewers(self):
        return self.get_queryset().order_by_rating_and_viewers()

    def search(self, search_query):
        return self.get_queryset().search(search_query)


class CommentManager(models.Manager):

    def comments_for_post(self, post):
        return super(CommentManager, self)\
            .filter(post=post, active=True)


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
    pub_date = models.DateTimeField(default=None, null=True, blank=True)
    last_modify_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserPostRelation', related_name='read_posts')
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

        if self.pub_date is None and self.is_published:
            self.pub_date = timezone.now()

        super().save(*args, **kwargs)

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_comments__post=self,
                                      post_comments__comment__active=True).count()

    @property
    def rating_value(self):
        if self.rating:
            return self.rating
        else:
            return 'No one rated this post yet'

    # @property
    # def likes(self):
    #     return self.objects.get().annotate(likes=Count(Case(When(userpostrelation__like=True, then=1))))

    @property
    def number_of_comments(self):
        return Comment.active_on_post(self.id)

    @property
    def is_published(self):
        return self.status

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=None, null=True)

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

    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    objects = CommentManager()

    def active_on_post(post_id):
        return Comment.objects.filter(post_id=post_id,
                                      active=True).count()
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
