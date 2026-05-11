from django.contrib import admin
from .models import Profile, Post, Community, CommunityMembership, DiscussionPod

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Community)
admin.site.register(CommunityMembership)
admin.site.register(DiscussionPod)