from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom user model extending AbstractUser
class User(AbstractUser):

    @property
    def is_service_provider(self):
        return self.user_role == "service_provider"

    @property
    def is_service_seeker(self):
        return self.user_role == "service_seeker"
    
    username = None
    email = models.EmailField(unique=True)

    # Choices for user roles
    ROLE_CHOICES = (
        ('service_seeker', 'Cliente'),
        ('service_provider', 'Proveedor'),
    )
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Choices for cities in the Medellin metropolitan area
    CITY_CHOICES = (
        ('medellin', 'Medellin'),
        ('envigado', 'Envigado'),
        ('bello', 'Bello'),
        ('sabaneta', 'Sabaneta'),
        ('itagui', 'Itagui'),
        ('la_estrella', 'La Estrella'),
        ('caldas', 'Caldas'),
        ('copacabana', 'Copacabana'),
        ('girardota', 'Girardota'),
        ('barbosa', 'Barbosa'),
    )
    user_city = models.CharField(max_length=20, choices=CITY_CHOICES)

    # Choices for user states
    VERIFICATION_CHOICES = (
        ('verificado', 'Verificado'),
        ('no_verificado', 'No Verificado'),
    )
    user_verification = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default='no_verificado')

    # Additional user fields
    user_birthdate = models.DateField(blank=False, null= False)
    user_phone = models.CharField(max_length=20, blank=False, null=False)
    user_address = models.CharField(max_length=100, blank=False, null=False)
    user_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    user_score = models.FloatField(default=5.0, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return f"{self.email} ({self.user_role})"


# Profile model for service providers
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="service_provider_profile")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Provider profile of {self.user.email}"

    

# Model for service provider experiences
class ProviderExperience(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="service_provider_experiences")
    experience_name = models.CharField(max_length=100, blank=False, null=False)
    experience_month_time = models.FloatField(blank=False, null=False, help_text="Duration in months")
    experience_company = models.CharField(max_length=100, blank=True, null=True)

    experience_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    experience_categories = models.ManyToManyField("searching.ServiceCategory", related_name="service_provider_experiences_categories")

    def __str__(self):
        return f"{self.experience_name} ({self.service_provider.user.username})"