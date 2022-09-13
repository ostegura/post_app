from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # User management
    path("api/users/", include("post_app.users.urls", namespace="users")),
    # Post management
    path("api/posts/", include("post_app.posts.urls", namespace="posts")),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
