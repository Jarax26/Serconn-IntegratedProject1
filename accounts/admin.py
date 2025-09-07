from django.contrib import admin
from .models import User, ServiceProvider, ProviderExperience

# Register your models here.
admin.site.register(User)
admin.site.register(ServiceProvider)
admin.site.register(ProviderExperience)
