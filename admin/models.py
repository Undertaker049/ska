from django.db import models
from django.contrib.auth.models import User


class UserActivity(models.Model):
    ACTION_TYPES = (
        ('login', 'Вход в систему'),
        ('logout', 'Выход из системы'),
        ('profile_update', 'Обновление профиля'),
        ('password_change', 'Смена пароля'),
        ('assessment_complete', 'Завершение оценки'),
        ('certificate_add', 'Добавление сертификата'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Действие пользователя'
        verbose_name_plural = 'Действия пользователей'

    def __str__(self):
        return f'{self.user.username} - {self.get_action_type_display()} - {self.created_at}'


class SystemMetrics(models.Model):
    date = models.DateField(auto_now_add=True)
    active_users = models.IntegerField(default=0)
    total_assessments = models.IntegerField(default=0)
    total_certificates = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Метрика системы'
        verbose_name_plural = 'Метрики системы'

    def __str__(self):
        return f'Метрики за {self.date}'