# from django.contrib.auth import get_user_model
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from rest_framework.authtoken.models import Token as DefaultToken
# from rest_framework import serializers

# CustomUser = get_user_model()


# class Token(DefaultToken):
#     custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='custom_auth_token', verbose_name=_('Custom User'))

#     class Meta:
#         verbose_name = _('Token')
#         verbose_name_plural = _('Tokens')


# class TokenSerializer(serializers.ModelSerializer):
#     custom_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

#     class Meta:
#         model = Token
#         fields = ('key', 'custom_user')
