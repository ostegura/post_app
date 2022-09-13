from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from post_app.users.models import User

from .serializers import (
    MyTokenObtainPairSerializer,
    UserActivitySerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class UserTokenObtainPairView(TokenObtainPairView):
    """Implementation of JWT Token obtaining with last_login update"""

    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list/retrieve actions for existing users.
    """

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()


class UserActivityViewSet(viewsets.ModelViewSet):
    """
    An APIView to get the latest user actions.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserActivitySerializer
    queryset = User.objects.all()


class UserRegistrationAPIView(APIView):
    """
    An APIView to register new users into the system.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    An APIView to logout users and 'blacklist' refresh token.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        response = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )

        try:
            token = RefreshToken(self.request.data["refresh"])
            token.blacklist()
        except KeyError:
            response.data = {
                "detail": "Refresh token was not included in request data."
            }
            response.status_code = status.HTTP_401_UNAUTHORIZED
        except (TokenError, AttributeError, TypeError) as error:
            if hasattr(error, "args"):
                if (
                    "Token is blacklisted" in error.args
                    or "Token is invalid or expired" in error.args
                ):
                    response.data = {"detail": error.args[0]}
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                else:
                    response.data = {"detail": "An error has occurred."}
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            else:
                response.data = {"detail": "An error has occurred."}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response
