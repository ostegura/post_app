from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from post_app.posts.api.views import PostViewSet
from post_app.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"posts", PostViewSet, basename="posts")


app_name = "api"
urlpatterns = router.urls
