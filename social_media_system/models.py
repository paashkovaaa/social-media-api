import os
import uuid

from django.utils.text import slugify

from user.models import User
from django.db import models


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/posts/", filename)


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    hashtag = models.ManyToManyField(Hashtag, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(null=True, upload_to=post_image_file_path)

    def __str__(self):
        return f"{self.user.email} at {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} liked {self.post.id}"

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} commented {self.post.id}"

    class Meta:
        ordering = ["-created_at"]


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.email} starts following {self.following.email}"

    class Meta:
        ordering = ["-created_at"]
