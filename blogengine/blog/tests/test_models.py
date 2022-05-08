from django.test import TestCase

from blog.models import Post, UserPostRelation
from users.models import User

# TODO: write more tests


class UserPostRelationModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')

        self.post_1 = Post.objects.create(
            title='sample cute title',
            slug='asbc_dfs 123*/&()%#@!?',
            body='cv',
            author=self.user_1,
        )
        self.post_2 = Post.objects.create(
            title='sample cuter title',
            slug='asbc)%#@!?',
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
