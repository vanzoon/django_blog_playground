from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status

from blog.models import UserPostRelation, Post, Tag
from blog.views import PostUpdateView
from users.models import User

# TODO: write tests for tag views, in progress


class PostViewsTestCase(TestCase):
    @staticmethod
    def setup_view(view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def setUp(self):
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.post_1 = Post.objects.create(title='sample cute title',
                                          body='cv',
                                          author=self.user_1,
                                          status=0,
                                          )
        self.post_2 = Post.objects.create(title='sample cuter title',
                                          body='asdf bpot',
                                          author=self.user_2,
                                          status=1,
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

    def test_get_posts(self):
        url = reverse('posts_list_url')
        response = self.client.get(url)
        self.assertTemplateUsed('blog/posts_list.html')
        self.assertTrue('is_paginated' in response.context)
        # because it is only 2 posts! We need more
        self.assertTrue(
            response.context['is_paginated'] is False)

        for post in range(2, 13):
            Post.objects.create(title=f'post number {post}',
                                body=f'blah blah blah {post}',
                                author=self.user_1,
                                status=1)

        url = reverse('posts_list_url')
        response = self.client.get(url)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('<Page 1 of 3>',
                        response.context['page_obj'])
        self.assertTrue(
            response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 4)

    def test_get_post_exist(self):
        url = reverse('post_detail_url',
                      kwargs={'slug': self.post_1.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(status.HTTP_200_OK,
                         response.status_code)

    def test_get_post_does_not_exist(self):
        url = reverse('post_detail_url',
                      kwargs={'slug': 'post_slug_that_does_not_exist'})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND,
                         response.status_code)

    def test_update_unauthorised_user_post_exist(self):
        rf = RequestFactory()
        url = reverse('post_update_url',
                      kwargs={'slug': self.post_1.slug})
        request = rf.post(url, data={'title': 'bhbh'})
        response = self.setup_view(PostUpdateView(), request)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         response.status_code)

    def test_update_authorised_user_post_does_not_exist(self):
        self.client.force_login(user=self.user_1)
        rf = RequestFactory()
        url = reverse('post_update_url',
                      kwargs={'slug': 'post_slug_that_does_not_exist'})
        request = rf.post(url, data={'title': 'bhbh'})
        view = self.setup_view(PostUpdateView(), request)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         view.context['Status-code'])

    def test_update_authorised_user_post_exist(self):
        self.client.force_login(self.user_1)
        rf = RequestFactory()
        url = reverse('post_update_url',
                      kwargs={'slug': self.post_1.slug})
        request = rf.post(url, data={'title': 'bhbh'})
        request.user = self.user_1
        # response = PostUpdateView.as_view()(request)

    def test_delete_authorised_user_post_does_not_exist(self):
        self.client.force_login(user=self.user_1)
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
                                          body='cv',
                                          author=self.user_1,
                                          )
        self.post_2 = Post.objects.create(title='sample cuter title',
                                          body='asdf bpot',
                                          author=self.user_2,
                                          )
        self.post_1.save()
        self.post_2.save()
        self.post_1.tags.add(self.tag_1, self.tag_2)
        self.post_2.tags.add(self.tag_2, self.tag_3)

    def test_tag_list(self):
        url = reverse('tags_list_url')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/tags_list.html')

    def test_tag_detail(self):
        url = reverse('tag_detail_url',
                      kwargs={'slug': self.tag_1.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/tag_detail.html')

    def test_tag_create(self):
        pass
        # url = reverse('tag_create_url')
        # response = self.client.post(url,
        #         kwargs={'title': 'exclamation4!!!!'})
        # self.assertTemplateUsed(response, 'blog/tag_create.html')
        # print(Tag.objects.get(title__iexact='exclamation4!!!!'))
        # self.assertEqual(status.HTTP_201_CREATED,
        #                  response.status_code)

    def test_tag_delete(self):
        pass
