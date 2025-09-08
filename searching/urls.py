from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_search_view, name='service_search'),
    path('add-service/', views.add_service, name='add_service'),
    path('provider/<int:provider_id>/', views.provider_detail_view, name='provider_detail'),
]
