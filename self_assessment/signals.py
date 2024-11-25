from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employees


@receiver(post_save, sender=User)
def create_employee_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Employees.objects.create(
            name=f"{instance.first_name} {instance.last_name}" or instance.username,
            role='admin'
        )