from django.urls import path

from post_app.posts.api import views

app_name = "posts"
urlpatterns = [
    path("analytics/", views.LikeFilterViewSet.as_view(), name="analytics"),
]
