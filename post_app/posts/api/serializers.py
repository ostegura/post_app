from rest_framework import serializers, validators

from post_app.posts.models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = ["id", "owner", "title", "content", "likes", "updated_at"]
        read_only_fields = ["id", "owner", "likes", "updated_at"]
        extra_kwargs = {"title": {"required": True}, "content": {"required": True}}


class PostLikeFilterSerializer(serializers.ModelSerializer):
    day = serializers.DateField()
    likes = serializers.IntegerField()

    class Meta:
        model = PostLike
        fields = (
            "day",
            "likes",
        )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = [
            "user",
            "post",
            "liked_at",
        ]
        read_only_fields = [
            "liked_at",
        ]
        validators = [
            validators.UniqueTogetherValidator(
                queryset=PostLike.objects.all(),
                fields=["post", "user"],
                message="Post is already liked.",
            )
        ]
