from django.db.models import Avg

from blog.models import UserPostRelation


def set_rating(post):
    post.rating = UserPostRelation.objects \
        .filter(post=post) \
        .only('rate') \
        .aggregate(rating=Avg('rate')) \
        .get('rating')
    post.save(update_fields=['rating'])
