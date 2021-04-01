from django.db.models import Avg

from blog.models import UserPostRelation


def set_rating(post):
    post.rating = UserPostRelation.objects \
        .filter(post=post) \
        .aggregate(rating=Avg('rate')) \
        .get('rating')
    post.save()
