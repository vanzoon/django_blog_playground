from django.contrib.auth.models import User
from django.db.models import JSONField, Count, Case, When, Avg
from django.test import TestCase

from api.serializers import PostSerializer
from blog.models import Post, UserPostRelation


class PostSerializerTestCase(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='user_1',
                                          first_name='john', last_name='brokk'
                                          )
        self.user_2 = User.objects.create(username='user_2',
                                          first_name='henz', last_name='nord'
                                          )
        self.user_3 = User.objects.create(username='user_3',
                                          first_name='', last_name=''
                                          )

        self.post_1 = Post.objects.create(title='bronks',
                                          body='first post body',
                                          author=self.user_1
                                          )
        self.post_2 = Post.objects.create(title='blah blah',
                                          body='love you guys',
                                          )

        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, like=True, rate=5,
                                        in_bookmarks=True)
        UserPostRelation.objects.create(user=self.user_2, post=self.post_1, like=False, rate=1,
                                        in_bookmarks=True)
        UserPostRelation.objects.create(user=self.user_3, post=self.post_1, like=True, rate=3)
        UserPostRelation.objects.create(user=self.user_2, post=self.post_2, like=True)

    def test_fields(self):
        posts = Post.objects.all().annotate(
            bookmarked_count=Count(Case(When(userpostrelation__in_bookmarks=True, then=1))),
            likes_count=Count(Case(When(userpostrelation__like=True, then=1))),
           # rating=Avg('userpostrelation__rate')
        ).order_by('id')
        # yeah, you need to lowercase class field......
        data = PostSerializer(posts, many=True).data
        expected_data = [
            {
                'id': self.post_1.id,
                'title': 'bronks',
                'body': 'first post body',
                'pub_date': self.post_1.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                'slug': self.post_1.slug,
                'bookmarked_count': 2,
                'likes_count': 2,
                'rating': '3.00',
                'author': 'user_1',
                'viewers': [
                    {
                        'first_name': 'john',
                        'last_name': 'brokk',
                    },
                    {
                        'first_name': 'henz',
                        'last_name': 'nord',
                    },
                    {
                        'first_name': '',
                        'last_name': '',
                    },
                ]
            },
            {
                'id': self.post_2.id,
                'title': 'blah blah',
                'body': 'love you guys',
                'pub_date': self.post_2.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                'slug': self.post_2.slug,
                'bookmarked_count': 0,
                'likes_count': 1,
                'rating': None,
                'author': '',  # at serializer we defined default='' for that field
                'viewers': [
                    {
                        'first_name': 'henz',
                        'last_name': 'nord',
                    },
                ]

            },
        ]
        self.assertEqual(expected_data, data)
