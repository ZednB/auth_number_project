from django.urls import path

from users.apps import UsersConfig
from users.views.referral import ActivateInviteView, UserReferralsView
from users.views.users import PhoneNumberAuthView, AuthCodeVerificationView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('auth/phone/', PhoneNumberAuthView.as_view(), name='phone_auth'),
    path('auth/code/', AuthCodeVerificationView.as_view(), name='code_verification'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('invite/activate/', ActivateInviteView.as_view(), name='activate_invite'),
    path('referrals/<str:phone_number>/', UserReferralsView.as_view(), name='user_referrals'),
]
