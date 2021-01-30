from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from blog.models import Post, UserPostRelation

class PostSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    likes_count_annotate = serializers.IntegerField(read_only=True)
    pub_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'pub_date', 'slug',
                  'likes_count', 'likes_count_annotate']

    def get_likes_count(self, instance):
        return UserPostRelation.objects.filter(post=instance, like=True).count()


class UserPostRelationSerializer(ModelSerializer):

    class Meta:
        model = UserPostRelation
        fields = ('post', 'like', 'in_bookmarks', 'rate')

