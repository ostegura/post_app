from django.utils import timezone


class UserLastRequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = request.user
        if user.is_authenticated:
            user.last_request = timezone.now()
            user.save(
                update_fields=[
                    "last_request",
                ]
            )

        return response
