from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'access' in request.COOKIES:
            token = request.COOKIES.get('access')
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

        response = self.get_response(request)
        return response