import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Count, Case, When, F
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.serializers import PostSerializer
from blog.models import Post, UserPostRelation
from users.models import User


class PostApiTestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.post_1 = Post.objects.create(title='sample cute title',
                                          slug='asbc_dfs 123*/&()%#@!?',
                                          body='cv',
                                          author=self.user_1,
                                          status=1
                                          )
        self.post_2 = Post.objects.create(title='draft post title',
                                          slug='gammagammagammma',
                                          body='mark my words, this post i will never publish',
                                          status=0
                                          )
        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, like=True)
        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, rate=5)
        UserPostRelation.objects.create(user=self.user_2, post=self.post_2, like=False)

    def test_get_send_valid_response(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        posts = Post.objects.all().annotate(
            author_name=F('author__username'),
            bookmarked_count=Count(Case(When(userpostrelation__in_bookmarks=True, then=1))),
            likes_count=Count(Case(When(userpostrelation__like=True, then=1))),
        )
        serialized_data = PostSerializer(posts, many=True).data
        self.assertEqual(serialized_data, response.data)
        self.assertEqual(serialized_data[0]['likes_count'], 0)
        self.assertEqual(serialized_data[0]['rating'], None)
        self.assertEqual(serialized_data[1]['likes_count'], 1)
        self.assertEqual(serialized_data[1]['rating'], '5.00')

    def test_get_response_used_optimized_queries(self):
        url = reverse('post-list')
        with CaptureQueriesContext(connection) as queries:
            self.client.get(url)
            self.assertEqual(3, len(queries))

    def test_create(self):
        self.client.force_login(self.user_1)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-list')
        data = {
            "title": "network switch",
            "body": "A network switch (also called switching hub, bridging hub, \
            and MAC bridge) is networking hardware that connects devices on \
            a computer network by using packet switching to receive and \
            forward data to the destination device.",
            "slug": "net_switch"
        }

        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(3, Post.objects.all().count())
        self.assertEqual(self.user_1, Post.objects.last().author)

    def test_delete(self):
        self.client.force_login(self.user_1)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-detail', args=(self.post_1.id,))

        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Post.objects.all().count())
        try:
            self.post_1.refresh_from_db()
        except ObjectDoesNotExist:
            pass

    def test_delete_not_author(self):
        self.client.force_login(self.user_2)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-detail', args=(self.post_1.id,))

        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Post.objects.all().count())
        self.post_1.refresh_from_db()
        self.assertEqual('sample cute title', self.post_1.title)
        self.assertEqual('cv', self.post_1.body)

    def test_delete_not_author_but_staff(self):
        self.user2 = User.objects.create(username='test_user2', is_staff=True)
        self.client.force_login(self.user2)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-detail', args=(self.post_1.id,))

        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Post.objects.all().count())
        try:
            self.post_1.refresh_from_db()
        except ObjectDoesNotExist:
            pass

    def test_update(self):
        self.client.force_login(self.user_1)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-detail', args=(self.post_1.id,))

        data = {
            "title": self.post_1.title,
            "body": "A network switch is networking hardware that connects devices \
             on a computer network by using packet switching to receive and \
             forward data to the destination device.",
            "slug": "blueredgreen"
        }

        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(2, Post.objects.all().count())

        self.post_1.refresh_from_db()
        self.assertGreater(self.post_1.last_modify_date, self.post_1.pub_date)

        self.assertEqual(data["body"], self.post_1.body)
        self.assertEqual(data["title"], self.post_1.title)

    def test_update_not_author(self):
        self.client.force_login(self.user_2)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-detail', args=(self.post_1.id,))

        data = {
            "title": self.post_1.title,
            "body": "bruh",
            "slug": "bluegreenred"
        }

        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Post.objects.all().count())

        self.post_1.refresh_from_db()

        self.assertEqual('cv', self.post_1.body)
        self.assertEqual('sample cute title', self.post_1.title)


class UserPostRelationTestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create(username='test_user_1')
        self.user_2 = User.objects.create(username='test_user_2')
        self.post_1 = Post.objects.create(title='sample cute title',
                                          slug='asbc_dfs 123*/&()%#@!?',
                                          body='cv',
                                          author=self.user_1)
        self.post_2 = Post.objects.create(title='sample cuter title',
                                          slug='asbc)%#@!?',
                                          body='asdf bpot',
                                          author=self.user_2)

    def test_like(self):
        url = reverse('userpostrelation-detail', args=(self.post_1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user_1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post_1.refresh_from_db()
        relation = UserPostRelation.objects.get(user=self.user_1, post=self.post_1)
        self.assertTrue(relation.like)

    def test_bookmark(self):
        url = reverse('userpostrelation-detail', args=(self.post_1.id,))
        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user_1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post_1.refresh_from_db()
        relation = UserPostRelation.objects.get(user=self.user_1, post=self.post_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userpostrelation-detail', args=(self.post_1.id,))
        data = {
            "rate": 4,
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user_1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserPostRelation.objects.get(user=self.user_1,
                                                post=self.post_1)
        self.assertEqual(relation.rate, 4)

    def test_rate_wrong(self):
        url = reverse('userpostrelation-detail', args=(self.post_1.id,))
        data = {
            "rate": 10,  # rate 10 does not exist
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user_1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
