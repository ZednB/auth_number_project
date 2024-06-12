from django.shortcuts import get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response

from users.models import User, Referral
from users.serializers.users import UserSerializer


class ActivateInviteView(views.APIView):
    """Активирует инвайт-код и устанавливает реферальную связь между пользователями."""
    def post(self, request):
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')

        user = get_object_or_404(User, phone_number=phone_number)
        referred_by = get_object_or_404(User, invite_code=invite_code)

        if user.referred_by:
            return Response({'error': 'Инвайт-код уже активирован'}, status=status.HTTP_400_BAD_REQUEST)

        user.referred_by = referred_by
        user.save()

        Referral.objects.create(user=referred_by, reffered_user=user)
        return Response({'message': 'Инвайт код активирован'}, status=status.HTTP_200_OK)


class UserReferralsView(views.APIView):
    """Возвращает список пользователей, которые ввели инвайт-код текущего пользователя."""
    def get(self, request, phone_number):
        user = get_object_or_404(User, phone_number=phone_number)
        referrals = user.refferals.all()
        return Response(UserSerializer(referrals, many=True).data)
