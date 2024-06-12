from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефона')
    invite_code = models.CharField(max_length=6, unique=True, **NULLABLE, verbose_name='Инвайт код')
    referred_by = models.ForeignKey('self', **NULLABLE, on_delete=models.SET_NULL, related_name='referrals')
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f"{self.phone_number}, {self.invite_code}"

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_users')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.user}, {self.referred_user}"

    class Meta:
        verbose_name = 'Реферал'
        verbose_name_plural = 'Рефералы'
