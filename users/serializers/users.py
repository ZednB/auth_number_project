from rest_framework import serializers

from users.models import User, Referral


class UserSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'invite_code', 'referred_by', 'referred_users']

    def get_referred_users(self, obj):
        referrals = Referral.objects.filter(user=obj)
        referred_users = [ref.referred_user.phone_number for ref in referrals]
        return referred_users
