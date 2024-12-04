from django.db import models

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