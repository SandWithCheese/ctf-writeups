from __future__ import annotations
from django.contrib.auth.models import AnonymousUser, User
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class JWTAuthMiddleware(MiddlewareMixin):
    """
    Reads JWT from HttpOnly cookies (jwt_access) and sets request.user accordingly,
    so your normal Django views can use request.user and login_required.
    """

    def process_request(self, request):
        request.jwt_user = None
        access_cookie_name = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'jwt_access')
        raw_token = request.COOKIES.get(access_cookie_name)
        if not raw_token:
            return  

        try:
            backend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'],
                                   signing_key=settings.SIMPLE_JWT['SIGNING_KEY'])
            data = backend.decode(raw_token, verify=True)
            user_id = data.get('user_id')
            if not user_id:
                return
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return
            request.user = user
            request.jwt_user = user
        except (InvalidToken, TokenError, KeyError):
            request.user = getattr(request, 'user', AnonymousUser())
            return
