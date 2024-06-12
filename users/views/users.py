import random

from rest_framework import views, status, generics
from rest_framework.response import Response

from users.models import User
from users.serializers.users import UserSerializer


class PhoneNumberAuthView(views.APIView):
    """Имитирует отправку 4-значного кода авторизации по номеру телефона."""
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Нужен номер телефона.'}, status=status.HTTP_400_BAD_REQUEST)

        # Имитация отправки кода
        auth_code = random.randint(1000, 9999)
        request.session['auth_code'] = auth_code
        request.session['phone_number'] = phone_number

        # Имитация задержки
        return Response({'message': 'Код авторизации отправлен', 'code': auth_code}, status=status.HTTP_200_OK)


class AuthCodeVerificationView(views.APIView):
    """Проверяет введенный код авторизации и создает пользователя, если он не существует."""
    def post(self, request):
        code = request.data.get('code')
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if str(code) == str(auth_code):
            user, created = User.objects.get_or_create(phone_number=phone_number)
            return Response({'message': 'Авторизация прошла успешно', 'user': UserSerializer(user).data},
                            status=status.HTTP_200_OK)
        return Response({'error': 'Неправильный код авторизации.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Позволяет получить и обновить профиль пользователя по номеру телефона."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone_number'
