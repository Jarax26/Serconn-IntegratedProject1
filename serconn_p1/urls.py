from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Vistas específicas
from searching import views as appViews
from accounts import views as accountViews

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views

from django.shortcuts import redirect


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Apps
    path("accounts/", include("accounts.urls")),   # manejo de cuentas
    path("search/", include("searching.urls")),   # búsqueda de servicios
    path("interactions/", include("interactions.urls")), # <--- AÑADIR ESTA LÍNEA
    # path("payments/", include("payments.urls")),

    # Autenticación
    path("", accountViews.login_view, name="login"),
    path("login/", accountViews.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),

    # Vistas de servicios
    path("provider/<int:provider_id>/", appViews.provider_detail_view, name="provider_detail"),
    # Cambia la siguiente línea
    path("dashboard/", appViews.dashboard_view, name="dashboard"),

    path("error/", views.error_page, name="error_page"),
]

# Archivos multimedia en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def handler404(request, exception=None):
    return redirect(f"/error/?code=404&message=Página%20no%20encontrada")

def handler500(request):
    return redirect(f"/error/?code=500&message=Error%20interno%20del%20servidor")

def handler403(request, exception=None):
    return redirect(f"/error/?code=403&message=Acceso%20denegado")

def handler400(request, exception=None):
    return redirect(f"/error/?code=400&message=Solicitud%20inválida")

# Registrar handlers globales
handler404 = handler404
handler500 = handler500
handler403 = handler403
handler400 = handler400