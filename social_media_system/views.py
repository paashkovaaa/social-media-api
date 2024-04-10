from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from social_media_system.models import Hashtag, Post, Like, Comment, Follow
from social_media_system.permissions import (
    IsOwnerOrReadOnly,
)
from social_media_system.serializers import (
    HashtagSerializer,
    PostListSerializer,
    PostSerializer,
    PostImageSerializer,
    LikeSerializer,
    CommentSerializer,
    FollowSerializer,
)


class HashtagViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Post.objects.all().select_related("user")

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                IsAuthenticatedOrReadOnly,
            ]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "upload_image":
            return PostImageSerializer
        return PostSerializer

    @action(detail=False, methods=["get"])
    def my_posts(self, request):
        """
        Retrieve posts of the authenticated user.
        """
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        hashtag = self.request.query_params.get("hashtag")
        queryset = self.queryset

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtag",
                type=OpenApiTypes.STR,
                description="Filter by hashtag (ex. ?hashtag=story)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LikeViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Like.objects.all().select_related("post")
        post_id = self.request.query_params.get("post_id")
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    serializer_class = LikeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    @action(detail=False, methods=["get"])
    def my_likes(self, request):
        """
        Retrieve liked posts of the authenticated user.
        """
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.all().select_related("post")
        post_id = self.request.query_params.get("post_id")
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    serializer_class = CommentSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    @action(detail=False, methods=["get"])
    def my_comments(self, request):
        """
        Retrieve commented posts of the authenticated user.
        """
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def post_comments(self, request, pk=None):
        """
        Retrieve all comments for a specific post.
        """
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def get_queryset(self):
        queryset = Follow.objects.all().select_related("follower")
        follower_id = self.request.query_params.get("follower_id")
        if follower_id:
            queryset = queryset.filter(follower_id=follower_id)
        return queryset

    @action(detail=False, methods=["get"])
    def followers(self, request):
        """
        Retrieve the list of followers for the authenticated user.
        """
        user = request.user
        followers = Follow.objects.filter(following=user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def following(self, request):
        """
        Retrieve the list of users followed by the authenticated user.
        """
        user = request.user
        following = Follow.objects.filter(follower=user)
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)
