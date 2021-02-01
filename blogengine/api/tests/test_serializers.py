from django.contrib.auth.models import User
from django.db.models import JSONField, Count, Case, When, Avg
from django.test import TestCase

from api.serializers import PostSerializer
from blog.models import Post, UserPostRelation


class PostSerializerTestCase(TestCase):

    def setUp(self):
        self.long_text = 'some loooooooo ooooooooooooo oooooooooooo ooooooooooo \
        oooooooooooooooo ooooo oooooooooong 150+ symbols text'

        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.user_3 = User.objects.create(username='user_3')

        self.post_1 = Post.objects.create(title=self.long_text,
                                          body='first post body',
                                          )
        self.post_2 = Post.objects.create(title='blah blah',
                                          body='love you guys',
                                          )

        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, like=True)
        UserPostRelation.objects.create(user=self.user_2, post=self.post_1, like=False)
        UserPostRelation.objects.create(user=self.user_3, post=self.post_1, like=True)

        UserPostRelation.objects.create(user=self.user_2, post=self.post_2, like=True)

        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, rate=5)
        UserPostRelation.objects.create(user=self.user_2, post=self.post_1, rate=1)
        UserPostRelation.objects.create(user=self.user_3, post=self.post_1, rate=3)

    def test_fields(self):
        posts = Post.objects.all().annotate(
            likes_count_annotate=
                Count(Case(When(userpostrelation__like=True, then=1))),
            rating=Avg('userpostrelation__rate')
        ).order_by('id')
        # yeah, you need to lowercase class field......
        data = PostSerializer(posts, many=True).data
        expected_data = [
            {
                'id': self.post_1.id,
                'title': self.long_text,
                'body': 'first post body',
                'pub_date': self.post_1.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                'slug': self.post_1.slug,
                'likes_count': 2,
                'likes_count_annotate': 2,
                'rating': '3.00',
            },
            {
                'id': self.post_2.id,
                'title': 'blah blah',
                'body': 'love you guys',
                'pub_date': self.post_2.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                'slug': self.post_2.slug,
                'likes_count': 1,
                'likes_count_annotate': 1,
                'rating': None,
            },
        ]
        self.assertEqual(expected_data, data)


