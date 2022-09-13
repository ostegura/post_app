from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from post_app.users.api import views

app_name = "users"
urlpatterns = [
    path("login/", views.UserTokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("register/", views.UserRegistrationAPIView.as_view(), name="register"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path(
        "activity/", views.UserActivityViewSet.as_view({"get": "list"}), name="activity"
    ),
]
