from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    name = "post_app.posts"
    verbose_name = _("Posts")
