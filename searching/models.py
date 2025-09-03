from django.db import models
from django.conf import settings

# Un modelo de perfil para ServiceProvider que se extiende del User de Django
class ServiceProvider(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    service_info = models.TextField(blank=True)
    rates = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='provider_profiles/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)
    services_offered = models.CharField(max_length=200, blank=True)
    # ...otros campos...

    def __str__(self):
        return self.user.username


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)


class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2) # FR-8




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

