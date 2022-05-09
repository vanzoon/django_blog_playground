from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.test import TestCase

from blog.models import Post, UserPostRelation
from users.models import User


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

        self.user_post_1 = UserPostRelation.objects.create(
            user=self.user_2, post=self.post_1, rate=1, in_bookmarks=True
        )
        UserPostRelation.objects.create(
            user=self.user_3, post=self.post_1, rate=2, like=True
        )
        self.user_post_2 = UserPostRelation.objects.create(
            user=self.user_3, post=self.post_1
        )

    def test_rating_is_valid_without_changes(self):
        self.assertEqual(1.50, self.post_1.rating)

    def test_rating_is_valid_after_new_user_rate(self):
        user_post = UserPostRelation.objects.create(
            user=self.user_1, post=self.post_1, in_bookmarks=True, like=True
        )
        user_post.rate = 5
        user_post.save(update_fields=['rate'])
        self.assertEqual(2.67, round(self.post_1.rating, 2))

    def test_rating_does_not_evaluate_without_changing_rate_field(self):
        self.user_post_1.rate = 6
        self.user_post_1.save()

        # instead of creating new signal specifically to set_rating() this testcase
        # limit oneself to checking indirect sign of executing of this method
        @receiver(pre_save, sender=Post)
        def catch_set_rating_execution(sender, **kwargs):
            raise AssertionError(
                '''Rate field is not actually changed but set_rating() executed anyway'''
            )

        self.user_post_1.rate = 6
        self.user_post_1.save()
