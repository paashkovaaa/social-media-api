from django.contrib import admin

from social_media_system.models import Hashtag, Post, Like, Comment, Follow

admin.site.register(Hashtag)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
