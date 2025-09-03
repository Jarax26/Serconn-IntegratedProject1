from django.contrib import admin
from .models import ServiceProvider, ServiceCategory, Service, ServiceRequest

admin.site.register(ServiceProvider)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceRequest)
