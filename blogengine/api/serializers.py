from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from blog.models import Post, UserPostRelation, Comment
from users.models import User


class PostViewersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PostCommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'name', 'email', 'body', 'active')


class PostSerializer(ModelSerializer):
    pub_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False,
                                         read_only=True)
    author = serializers.CharField(source='author.username', default='', read_only=True)
    bookmarked_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    viewers = PostViewersSerializer(many=True, read_only=True)
    comments = PostCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'pub_date', 'slug', 'bookmarked_count',
                  'likes_count', 'rating', 'author', 'viewers', 'comments')


class UserPostRelationSerializer(ModelSerializer):

    class Meta:
        model = UserPostRelation
        fields = ('post', 'like', 'in_bookmarks', 'rate')
