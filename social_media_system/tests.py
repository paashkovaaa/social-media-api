from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from social_media_system.models import Post, Like, Comment, Follow
from social_media_system.serializers import (
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    FollowSerializer,
)


class SocialMediaViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password123"
        )
        self.client.force_authenticate(self.user)

    def test_create_post(self):
        url = "/api/social_media/posts/"
        data = {"content": "Test post"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().content, "Test post")

    def test_create_like(self):
        post = Post.objects.create(user=self.user, content="Test post")
        url = "/api/social_media/likes/"
        data = {"post": post.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().post, post)

    def test_create_comment(self):
        post = Post.objects.create(user=self.user, content="Test post")
        url = "/api/social_media/comments/"
        data = {"post": post.id, "content": "Test comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().post, post)

    def test_create_follow(self):
        user_to_follow = get_user_model().objects.create_user(
            email="user@example.com", password="password123"
        )
        url = "/api/social_media/follows/"
        data = {"following": user_to_follow.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(Follow.objects.get().follower, self.user)
