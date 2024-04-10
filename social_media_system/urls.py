from django.urls import path, include
from rest_framework import routers

from social_media_system.views import (
    PostViewSet,
    HashtagViewSet,
    LikeViewSet,
    CommentViewSet,
    FollowViewSet,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
router.register("likes", LikeViewSet, basename="like")
router.register("comments", CommentViewSet, basename="comment")
router.register("follows", FollowViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social_media_system"
