from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from .models import ServiceCategory, Service
from accounts.models import ServiceProvider
from interactions.models import Booking
from .forms import ServiceForm
from accounts.models import User
from datetime import datetime

@login_required
def dashboard_view(request):
    """
    Muestra el dashboard correspondiente según el rol del usuario.
    """
    if request.user.is_service_seeker:
        # Busca las reservas donde el usuario es el solicitante
        bookings = Booking.objects.filter(chat__seeker=request.user).order_by('-start_time')
        return render(request, 'seeker_dashboard.html', {'bookings': bookings})
    
    elif request.user.is_service_provider:
        # Busca las reservas donde el usuario es el proveedor
        bookings = Booking.objects.filter(chat__provider=request.user).order_by('-start_time')
        return render(request, 'provider_dashboard.html', {'bookings': bookings})

    # Si no tiene un rol definido, lo redirige a la búsqueda
    return redirect('service_search')

def service_search_view(request):
    """
    Vista principal para la búsqueda de servicios.
    """
    categories = ServiceCategory.objects.all()
    providers = ServiceProvider.objects.select_related("user").filter(services__isnull=False).distinct()
    
    query = request.GET.get('query')
    category = request.GET.get('category')
    city = request.GET.get('city')
    availability_start_str = request.GET.get('availability_start')
    availability_end_str = request.GET.get('availability_end')

    if query:
        providers = providers.filter(
            Q(description__icontains=query) |  
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(services__name__icontains=query) |
            Q(services__description__icontains=query)
        ).distinct()

    if category:
        providers = providers.filter(services__category__name=category).distinct()

    if city:
        providers = providers.filter(user__user_city=city).distinct()

    if availability_start_str and availability_end_str:
        try:
            availability_start = datetime.fromisoformat(availability_start_str)
            availability_end = datetime.fromisoformat(availability_end_str)

            # Lógica de filtro corregida: Busca proveedores cuya disponibilidad
            # contenga completamente el rango de tiempo solicitado.
            providers = providers.filter(
                availability__start_time__lte=availability_start,
                availability__end_time__gte=availability_end
            ).distinct()
        except (ValueError, TypeError):
            # Ignorar si el formato de fecha es inválido
            pass

    context = {
        'categories': categories,
        'providers': providers,
        'query': query,
        'selected_category': category,
        'selected_city': city,
        'cities': User.CITY_CHOICES,
        'availability_start': availability_start_str,
        'availability_end': availability_end_str,
    }
    return render(request, 'service_search.html', context)


def provider_detail_view(request, provider_id):
    """
    Vista para mostrar el perfil detallado de un proveedor.
    """
    try:
        provider = get_object_or_404(ServiceProvider, pk=provider_id)
    except Http404:
        return render(request, '404.html')

    services_offered = Service.objects.filter(provider=provider)

    context = {
        'provider': provider,
        'services_offered': services_offered,
    }
    return render(request, 'provider_detail.html', context)

@login_required
def add_service(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = provider
            service.save()
            return redirect("profile")
    else:
        form = ServiceForm()
    return render(request, "add_service.html", {"form": form})