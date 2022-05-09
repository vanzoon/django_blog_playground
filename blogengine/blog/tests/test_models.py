from django.test import TestCase

from blog.models import Post, UserPostRelation, Tag, Comment
from users.models import User

# TODO: write more tests


class UserPostRelationModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.post_1 = Post.objects.create(
            title='sample cute title',
            body='cv',
            author=self.user_1,
        )
        self.post_2 = Post.objects.create(
            title='sample cuter title',
            body='asdf bpot',
            author=self.user_2,
        )
        self.user_post_1 = UserPostRelation.objects.create(
            user=self.user_1, post=self.post_1, like=True
        )
        UserPostRelation.objects.create(
            user=self.user_1, post=self.post_1, rate=5
        )
        UserPostRelation.objects.create(
            user=self.user_2, post=self.post_2, like=False
        )


class PostManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.admin = User.objects.create(username='admin')

        self.tag_1 = Tag.objects.create(title='bruh TITLE')
        self.tag_2 = Tag.objects.create(title='bruh')

        self.post_1 = Post.objects.create(
            title='sample cute title',
            body='cv',
            author=self.user_1,
            status=0,
        )
        self.post_2 = Post.objects.create(
            title='nuclear winter',
            body='asdf pants',
            author=self.user_2,
            status=1,
        )

        self.post_3 = Post.objects.create(
            title='cold TTTTTTitle',
            body='it is cold out there xxTiTLExxTitlexx bpot',
            author=self.admin,
            status=1,
        )

        self.post_4 = Post.objects.create(
            title='sample tremendous case',
            body='asdf bpot',
            author=self.user_2,
            status=0,
        )

        self.post_5 = Post.objects.create(
            title=' super goth',
            body=' blep mlem bpot',
            author=self.admin,
            status=1,
        )

        self.post_1.save()
        self.post_2.save()
        self.post_3.save()
        self.post_4.save()
        self.post_5.save()

        self.post_2.tags.set([self.tag_1, self.tag_2])
        self.post_5.tags.set([self.tag_2])

    def test_get_published(self):
        published_query = Post.objects.get_published().order_by('id')
        actually_published = [self.post_2, self.post_3, self.post_5]
        # not_published = [self.post_1, self.post_4]
        self.assertEqual(actually_published, list(published_query))

    def test_filter_author_admin(self):
        posted_by_admin = Post.objects.filter_author_admin().order_by('id')
        actually_posted_by_admin = [self.post_3, self.post_5]
        # posted_by_others = [self.post_1, self.post_2, self.post_4]
        self.assertEqual(actually_posted_by_admin,
                         list(posted_by_admin))

    def test_search(self):
        example_search_qs = Post.objects.search('title').order_by('id')
        actually_searched_for = [self.post_1, self.post_3]
        self.assertEqual(actually_searched_for,
                         list(example_search_qs))


class PostTestCase(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.admin = User.objects.create(username='admin')

        self.tag_1 = Tag.objects.create(title='bruh TITLE')
        self.tag_2 = Tag.objects.create(title='bruh')

        self.post_1 = Post.objects.create(
            title='sample cute title',
            body='cv',
            author=self.user_1,
            status=0,
        )
        self.post_2 = Post.objects.create(
            title='nuclear winter',
            body='asdf pants',
            author=self.user_2,
            status=1,
        )

        self.post_3 = Post.objects.create(
            title='cold TTTTTTitle',
            body='it is cold out there xxTiTLExxTitlexx bpot',
            author=self.admin,
            status=1,
        )

        self.post_4 = Post.objects.create(
            title='sample tremendous case',
            body='asdf bpot',
            author=self.user_2,
            status=0,
        )

        self.post_5 = Post.objects.create(
            title=' super goth',
            body=' blep mlem bpot',
            author=self.admin,
            status=1,
        )

        self.post_1.save()
        self.post_2.save()
        self.post_3.save()
        self.post_4.save()
        self.post_5.save()

        self.post_2.tags.set([self.tag_1, self.tag_2])
        self.post_5.tags.set([self.tag_2])

    def test_number_of_comments(self):
        self.comment_1 = Comment.objects.create(
            post=self.post_1, email='cadence@mail.com',
            name='bob', active=1)

        self.comment_2 = Comment.objects.create(
            post=self.post_1, email='savory@mail.com',
            name='bob marley', active=1)

        self.comment_3 = Comment.objects.create(
            post=self.post_2, email='savory@jojo.com',
            name='trade with me', active=1)

        self.comment_4 = Comment.objects.create(
            post=self.post_2, email='savory@jojo.jp',
            name='anti anime anime club', active=0)

        comments_on_post_1 = self.post_1.number_of_comments
        actually_comments_on_post_1 = 2
        self.assertEqual(actually_comments_on_post_1,
                         comments_on_post_1)

        comments_on_post_2 = self.post_2.number_of_comments
        actually_comments_on_post_2 = 1
        self.assertEqual(actually_comments_on_post_2,
                         comments_on_post_2)

        comments_on_post_3 = self.post_3.number_of_comments
        actually_comments_on_post_3 = 0
        self.assertEqual(actually_comments_on_post_3,
                         comments_on_post_3)
