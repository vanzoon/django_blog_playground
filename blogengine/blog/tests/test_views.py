import json

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status

from blog.models import UserPostRelation, Post, Tag
from blog.views import TagDetailView, TagCreateView
from users.models import User

# TODO: write tests for tag views


class PostViewsTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.post_1 = Post.objects.create(title='sample cute title',
                                          slug='asbc_dfs 123*/&()%#@!?',
                                          body='cv',
                                          author=self.user_1,
                                          )
        self.post_2 = Post.objects.create(title='sample cuter title',
                                          slug='asbc)%#@!?',
                                          body='asdf bpot',
                                          author=self.user_2,
                                          )

        UserPostRelation.objects.create(user=self.user_1,
                                        post=self.post_1,
                                        like=True)
        UserPostRelation.objects.create(user=self.user_1,
                                        post=self.post_1,
                                        rate=5)
        UserPostRelation.objects.create(user=self.user_2,
                                        post=self.post_2,
                                        like=False)

    def test_get_post_exist(self):
        url = reverse('post_detail_url',
                      kwargs={'slug': self.post_1.slug})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code)

    def test_get_post_does_not_exist(self):
        url = reverse('post_detail_url',
                      kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND,
                         response.status_code)

    def test_update_unauthorised_user_post_exist(self):
        url = reverse('post_update_url',
                      kwargs={'slug': self.post_1.slug})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         response.status_code)

    def test_update_authorised_user_post_does_not_exist(self):
        url = reverse('post_update_url',
                      kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         response.status_code)

    def test_delete_authorised_user_post_does_not_exist(self):
        url = reverse('post_delete_url',
                      kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         response.status_code)

    def test_delete_user_not_owner_post_exist(self):
        self.client.force_login(user=self.user_1)
        url = reverse('post_delete_url',
                      kwargs={'slug': self.post_2.slug})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED,
                         response.status_code)

    def test_delete_user_owner_post_exist(self):
        self.client.force_login(user=self.user_1)
        url = reverse('post_delete_url',
                      kwargs={'slug': self.post_1.slug})
        response = self.client.delete(url)
        try:
            self.post_1.refresh_from_db()
        except ObjectDoesNotExist:
            pass
        self.assertEqual(status.HTTP_204_NO_CONTENT,
                         response.status_code)


class TagViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.tag_1 = Tag.objects.create(title='exclamation1')
        self.tag_2 = Tag.objects.create(title='exclamation2')
        self.tag_3 = Tag.objects.create(title='exclamation3')

        self.post_1 = Post.objects.create(title='sample cute title',
                                          slug='asbc_dfs 123*/&()%#@!?',
                                          body='cv',
                                          author=self.user_1,
                                          # tags=(self.tag_1, self.tag_2)
                                          )
        self.post_2 = Post.objects.create(title='sample cuter title',
                                          slug='asbc)%#@!?',
                                          body='asdf bpot',
                                          author=self.user_2,
                                          # tags=(self.tag_2, self.tag_3)
                                          )
        self.post_1.save()
        self.post_2.save()
        self.post_1.tags.add(self.tag_1, self.tag_2)
        self.post_2.tags.add(self.tag_2, self.tag_3)

    def test_tag_detail(self):
        factory = RequestFactory()
        request = factory.get('blog/tag/')
        response = TagDetailView.as_view()(request, slug='exclamation1')
        print(response.content)
        # self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.tag_1.title, response.content['title'])

    def test_tag_create(self):
        factory = RequestFactory()
        data = {
            "title": "bruh",
            "slug": "bruh"
        }
        json_data = json.dumps(data)

        request = factory.put('blog/tag/create/', data=json_data,
                              content_type='application/json')
        request.user = self.user_1
        response = TagCreateView.as_view()(request, slug='awer')
        # print(dir(response))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertEqual('blog/tag/bruh/', response)
        # self.assertEqual('blog/tag/create/', response.url)
        created_tag = Tag.objects.get(slug='bruh')
        self.assertEqual(data["title"], created_tag)

    def test_tag_delete(self):
        pass
