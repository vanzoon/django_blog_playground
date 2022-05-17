from django.db.models import Count, Case, When, F
from django.test import TestCase

from api.serializers import PostSerializer
from blog.models import Post, UserPostRelation
from users.models import User

# TODO: add some comment data


class PostSerializerTestCase(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='user_1',
                                          first_name='john',
                                          last_name='brokk'
                                          )
        self.user_2 = User.objects.create(username='user_2',
                                          first_name='henz',
                                          last_name='nord'
                                          )
        self.user_3 = User.objects.create(username='user_3',
                                          first_name='',
                                          last_name=''
                                          )

        self.post_1 = Post.objects.create(title='bronks',
                                          body='first post body',
                                          author=self.user_1,
                                          status=1,
                                          )
        self.post_2 = Post.objects.create(title='blah blah',
                                          body='love you guys',
                                          status=0,
                                          )

        UserPostRelation.objects.create(user=self.user_1,
                                        post=self.post_1,
                                        like=True,
                                        rate=5,
                                        in_bookmarks=True)
        UserPostRelation.objects.create(user=self.user_2,
                                        post=self.post_1,
                                        like=False,
                                        rate=1,
                                        in_bookmarks=True)
        UserPostRelation.objects.create(user=self.user_3,
                                        post=self.post_1,
                                        like=True, rate=3)
        UserPostRelation.objects.create(user=self.user_2,
                                        post=self.post_2,
                                        like=True)

    def test_fields(self):
        posts = Post.objects.all().annotate(
            author_name=F('author__username'),
            bookmarked_count=Count(Case(When(
                userpostrelation__in_bookmarks=True, then=1))
            ),
            likes_count=Count(Case(When(
                userpostrelation__like=True, then=1))
            ),
        ).order_by('id')
        data = PostSerializer(posts, many=True).data
        expected_data = [
            {
                'id': self.post_1.id,
                'title': 'bronks',
                'body': 'first post body',
                # 'status': 1, PUBLISHED
                'pub_date': self.post_1.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                'slug': self.post_1.slug,
                'bookmarked_count': 2,
                'likes_count': 2,
                'rating': '3.00',
                'author_name': 'user_1',
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
                ],
                'comments': []
            },
            {
                'id': self.post_2.id,
                'title': 'blah blah',
                'body': 'love you guys',
                # 'status': 0, DRAFT
                'pub_date': None,  # THEREFORE, NO PUBLISHED DATE
                'slug': self.post_2.slug,
                'bookmarked_count': 0,
                'likes_count': 1,
                'rating': None,
                'author_name': None,
                'viewers': [
                    {
                        'first_name': 'henz',
                        'last_name': 'nord',
                    },
                ],
                'comments': []
            },
        ]
        self.assertEqual(expected_data, data)
