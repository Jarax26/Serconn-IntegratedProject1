from django.contrib import admin
from .models import ServiceCategory, Service, ServiceRequest


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "category", "rate")
    search_fields = ("name", "description", "provider__user__email", "provider__user__first_name")
    list_filter = ("category",)
    autocomplete_fields = ("provider", "category")


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("seeker", "status", "created_at", "seeker_confirmed", "provider_confirmed")
    search_fields = ("seeker__email", "seeker__first_name", "seeker__last_name", "description")
    list_filter = ("status", "created_at")
    date_hierarchy = "created_at"
