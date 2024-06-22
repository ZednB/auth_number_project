import random
import string
import time

from django.shortcuts import get_object_or_404
from rest_framework import views, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers.users import UserSerializer

auth_codes = {}


class PhoneNumberAuthView(views.APIView):
    """Имитирует отправку 4-значного кода авторизации по номеру телефона."""
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Нужен номер телефона.'}, status=status.HTTP_400_BAD_REQUEST)

        # Имитация отправки кода
        auth_code = ''.join(random.choices(string.digits, k=4))
        auth_codes[phone_number] = auth_code

        # Имитация задержки
        time.sleep(2)

        return Response({'message': 'Код авторизации отправлен', 'auth_code': auth_code}, status=status.HTTP_200_OK)


class AuthCodeVerificationView(views.APIView):
    """Проверяет введенный код авторизации и создает пользователя, если он не существует."""
    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if not phone_number or not auth_code:
            return Response({'error': 'Укажите номер телефона и код авторизации.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if auth_codes.get(phone_number) != auth_code:
            return Response({'error': 'Неправильный код авторизации.'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.set_unusable_password()
            user.save()
        del auth_codes[phone_number]
        return Response({'message': 'Авторизация прошла успешно', 'user': UserSerializer(user).data},
                        status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Позволяет получить и обновить профиль пользователя по номеру телефона."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class ObtainTokenView(TokenObtainPairView):
    """Возвращает JWT-токен для указанного номера телефона."""

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Укажите номер телефона.'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number, defaults={'username': phone_number})
        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'refresh': str(refresh),
            'access': str(access_token)
        })
