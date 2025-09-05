from django.db import models
from django.contrib.auth.models import User

# Un modelo de perfil para ServiceProvider que se extiende del User de Django
class ServiceProvider(models.Model):
    user = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profiles')
    description = models.TextField()
    is_verified = models.BooleanField(default=False)


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)


class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2) # FR-8


