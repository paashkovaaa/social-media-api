from rest_framework import serializers

from social_media_system.models import Hashtag, Post, Like, Comment, Follow
from user.models import User


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    hashtag = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "content", "hashtag", "created_at", "images")


class PostListSerializer(PostSerializer):

    class Meta:
        model = Post
        fields = ("id", "user", "content", "hashtag", "created_at")


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "images")


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Like
        fields = ("id", "post", "user", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ("id", "post", "user", "content", "created_at")


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "created_at")
