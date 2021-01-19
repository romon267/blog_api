from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, UserFollowing

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'posts', 'following', 'followers']


    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'# ['url', 'id', 'author', 'content']


class UserFollowingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'


class FollowingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['id', 'following_user_id', 'created']

class FollowersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['id', 'user_id', 'created']