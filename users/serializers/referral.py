from rest_framework import serializers

from users.models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'user', 'referred_user', 'created_at']
