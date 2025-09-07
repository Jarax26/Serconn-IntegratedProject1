"""
URL configuration for serconn_p1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

<<<<<<< HEAD
from searching import views as appViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('searching.urls')),  # Las URLs de la app 'searching' serán la página de inicio
    # path('accounts/', include('accounts.urls')),
    # path('payments/', include('payments.urls')),
    # path('interactions/', include('interactions.urls')),
=======
from serconn_app import views as appViews
from serconn_app.views import seeker_dashboard, confirm_service
from django.contrib.auth import views as auth_views
from serconn_app.views import provider_profile, register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", appViews.service_search_view, name="service_search"),
    path("provider/<int:provider_id>/", appViews.provider_detail_view, name="provider_detail"),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('service/confirm/<int:pk>/', confirm_service, name='confirm_service'),
    path('provider/profile/', provider_profile, name='provider_profile'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirige a la raíz
]

urlpatterns += [
    path('dashboard/', seeker_dashboard, name='seeker_dashboard'),
>>>>>>> c1cd290 (Avance chao)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
