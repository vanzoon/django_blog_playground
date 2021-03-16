from django.contrib.auth.models import User
from django.test import TestCase


from api.logic import set_rating
from blog.models import Post, UserPostRelation


class SetRatingTestCase(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='user_1',
                                          first_name='john', last_name='brokk'
                                          )
        self.user_2 = User.objects.create(username='user_2',
                                          first_name='henz', last_name='nord')

        self.user_3 = User.objects.create(username='user_3',
                                          first_name='', last_name='')

        self.post_1 = Post.objects.create(title='bronks',
                                          body='first post body',
                                          author=self.user_1)
        self.post_1 = Post.objects.create(title='blah blah',
                                          body='love you guys',)

        UserPostRelation.objects.create(user=self.user_2, post=self.post_1,
                                        like=False, rate=1, in_bookmarks=True)

    def test_valid_rating_is_returned(self):
        self.assertEqual(1.00, self.post_1.rating)
        user_post_2 = UserPostRelation.objects.create(user=self.user_1,
                                                      post=self.post_1,
                                                      in_bookmarks=True,
                                                      like=True)
        user_post_2.rate = 4
        user_post_2.save()
        # set_rating(self.post_1)
        self.assertEqual(2.50, self.post_1.rating)
        UserPostRelation.objects.create(user=self.user_3, post=self.post_1,
                                        like=True, rate=2)
        self.assertEqual(2.33, round(self.post_1.rating, 2))

    def test_executes_only_after_entry_creation_or_updating_rate_field(self):
        pass
