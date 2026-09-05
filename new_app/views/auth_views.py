from django.conf import settings
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from new_app.serializers.register import RegisterSerializer

ACCESS_COOKIE_MAX_AGE = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
REFRESH_COOKIE_MAX_AGE = int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get('access')
            refresh = response.data.get('refresh')

            response.set_cookie(key='access_token',value=access,httponly=True,secure=not settings.DEBUG,samesite='Lax',
                                                                    max_age=ACCESS_COOKIE_MAX_AGE,)
            response.set_cookie(key='refresh_token',value=refresh,httponly=True,secure=not settings.DEBUG,samesite='Lax',
                                                                    max_age=REFRESH_COOKIE_MAX_AGE,)
        return response


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not in cookies.'},status=status.HTTP_401_UNAUTHORIZED,)

        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except (TokenError, ValidationError):
            return Response({'detail': 'Refresh token invalid or expired.'},status=status.HTTP_401_UNAUTHORIZED,)

        access = serializer.validated_data['access']
        response = Response({'access': access}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=ACCESS_COOKIE_MAX_AGE,
        )

        new_refresh = serializer.validated_data.get('refresh')
        if new_refresh:
            response.set_cookie(key='refresh_token',value=new_refresh,httponly=True,secure=not settings.DEBUG,
                                                                samesite='Lax',max_age=REFRESH_COOKIE_MAX_AGE,)
        return response



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh_token')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        except (TokenError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)