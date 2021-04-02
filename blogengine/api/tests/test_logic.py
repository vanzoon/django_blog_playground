from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.test import TestCase


from api.logic import set_rating
from blog.models import Post, UserPostRelation

# TODO: write test for rating field


class SetRatingTestCase(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(
            username='user_1', first_name='john', last_name='brokk'
        )
        self.user_2 = User.objects.create(
            username='user_2', first_name='henz', last_name='nord'
        )

        self.user_3 = User.objects.create(
            username='user_3', first_name='', last_name=''
        )

        self.post_1 = Post.objects.create(
            title='bronks', body='first post body', author=self.user_1
        )
        self.post_1 = Post.objects.create(
            title='blah blah', body='love you guys'
        )

        UserPostRelation.objects.create(
            user=self.user_2, post=self.post_1, like=False, rate=1, in_bookmarks=True
        )
        UserPostRelation.objects.create(
            user=self.user_3, post=self.post_1, like=True, rate=2
        )

    def test_rating_is_valid(self):
        self.assertEqual(1.50, self.post_1.rating)

    def test_rating_is_valid_after_new_user_rate(self):
        user_post = UserPostRelation.objects.create(
            user=self.user_1, post=self.post_1, in_bookmarks=True, like=True
        )
        user_post.rate = 5
        user_post.save(update_fields=['rate'])
        # set_rating(self.post_1)
        self.assertEqual(2.67, round(self.post_1.rating, 2))

    def test_rating_evaluates_only_after_entry_creation_or_update_rate_field(self):
        pass
