from django.db.models import Avg

from blog.models import UserPostRelation

# Note/todo: you may want to rename "rating" to "_rating" and refactor used quires
# AND|OR make @property.setter

def set_rating(post):
    post.rating = UserPostRelation.objects \
        .filter(post=post) \
        .aggregate(rating=Avg('rate')) \
        .get('rating')
    post.save(update_fields=['rating'])
