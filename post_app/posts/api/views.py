from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from post_app.posts.api.serializers import (
    PostLikeFilterSerializer,
    PostLikeSerializer,
    PostSerializer,
)
from post_app.posts.models import Post, PostLike
from post_app.posts.permissions import IsPostOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    Provides create/retrieve/update/delete actions for posts.
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "DELETE":
            permission_classes = [
                permissions.IsAuthenticated,
                IsPostOwnerOrReadOnly,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    @action(methods=["POST", "DELETE"], detail=True)
    def likes(self, request, pk=None):
        post = self.get_object()
        if request.method == "POST":
            data = dict(user=self.request.user.pk, post=post.pk)
            serializer = PostLikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            try:
                post_like = PostLike.objects.get(
                    user=self.request.user.pk, post=post.pk
                )
                post_like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except PostLike.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostLikeFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="liked_at", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="liked_at", lookup_expr="lte")

    class Meta:
        model = PostLike
        fields = [
            "date_from",
            "date_to",
        ]


class LikeFilterViewSet(generics.ListAPIView):
    queryset = (
        PostLike.objects.extra(select={"day": "date(liked_at)"})
        .values("day")
        .annotate(likes=Count("liked_at"))
        .order_by("-day")
    )
    serializer_class = PostLikeFilterSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    filterset_class = PostLikeFilter
