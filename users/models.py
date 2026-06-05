from django.db import models


class UsersPlaceholder(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'