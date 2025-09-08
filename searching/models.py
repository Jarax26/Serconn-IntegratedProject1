from django.db import models
from django.conf import settings
from accounts.models import ServiceProvider


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Categoría de servicio"
        verbose_name_plural = "Categorías de servicios"


class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]

    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    seeker_confirmed = models.BooleanField(default=False)
    provider_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seeker.username} - {self.status}"

