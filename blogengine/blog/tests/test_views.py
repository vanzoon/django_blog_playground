from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status

from blog.views import *

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
        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, like=True)
        UserPostRelation.objects.create(user=self.user_1, post=self.post_1, rate=5)
        UserPostRelation.objects.create(user=self.user_2, post=self.post_2, like=False)

    def test_get_post_exist(self):
        url = reverse('post_detail_url', kwargs={'slug': self.post_1.slug})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_post_does_not_exist(self):
        url = reverse('post_detail_url', kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_unauthorised_user_post_exist(self):
        url = reverse('post_update_url', kwargs={'slug': self.post_1.slug})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_authorised_user_post_does_not_exist(self):
        url = reverse('post_update_url', kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_authorised_user_post_does_not_exist(self):
        url = reverse('post_delete_url', kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_user_not_owner_post_exist(self):
        self.client.force_login(user=self.user_1)
        url = reverse('post_delete_url', kwargs={'slug': self.post_2.slug})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_delete_user_owner_post_exist(self):
        self.client.force_login(user=self.user_1)
        url = reverse('post_delete_url', kwargs={'slug': self.post_1.slug})
        response = self.client.delete(url)
        try:
            self.post_1.refresh_from_db()
        except ObjectDoesNotExist:
            pass
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


class TagViewsTestCase(TestCase):
    pass
