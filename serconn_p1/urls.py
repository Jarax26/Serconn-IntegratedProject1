from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Vistas específicas
from searching import views as appViews
from accounts import views as accountViews

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Apps
    path("accounts/", include("accounts.urls")),   # manejo de cuentas
    path("search/", include("searching.urls")),   # búsqueda de servicios
    # path("payments/", include("payments.urls")),
    # path("interactions/", include("interactions.urls")),

    # Autenticación
    path("", accountViews.login_view, name="login"),
    path("login/", accountViews.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),

    # Vistas de servicios
    path("provider/<int:provider_id>/", appViews.provider_detail_view, name="provider_detail"),
    path("dashboard/", appViews.seeker_dashboard, name="seeker_dashboard"),
]

# Archivos multimedia en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
