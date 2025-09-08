from django.contrib import admin
from .models import User, ServiceProvider, ProviderExperience
from searching.models import Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1   # muestra un campo extra para añadir un servicio nuevo
    fields = ("name", "category", "description", "rate")
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "user_role", "user_city", "user_verification")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("user_role", "user_city", "user_verification")


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("user", "description")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    inlines = [ServiceInline]  # <-- aquí se agregan los servicios inline


@admin.register(ProviderExperience)
class ProviderExperienceAdmin(admin.ModelAdmin):
    list_display = ("experience_name", "service_provider", "experience_company")
    search_fields = ("experience_name", "experience_company")
    list_filter = ("experience_categories",)
