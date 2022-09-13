from django.contrib import admin
from django.db.models import Count

from .models import Post, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "title",
        "likes_count",
        "created_at",
        "updated_at",
    )
    search_fields = ["owner", "title"]

    def likes_count(self, obj):
        return obj.likes_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(likes_count=Count("likes"))
        return queryset


@admin.register(PostLike)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "liked_at",
    )
    search_fields = ["user__pk"]
