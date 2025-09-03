from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceProvider, ServiceCategory, Service
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from .forms import ServiceProviderForm

# Vistas para la sección de búsqueda y perfiles
def service_search_view(request):
    """
    Vista principal para la búsqueda de servicios.
    """
    # Obtener todas las categorías de servicio para el menú desplegable
    categories = ServiceCategory.objects.all()
    
    # Inicializar la lista de proveedores
    providers = ServiceProvider.objects.all()
    query = request.GET.get('query', None)
    category = request.GET.get('category', None)

    if query:
        providers = providers.filter(
            Q(service_info__icontains=query) |
            Q(profession__icontains=query) |
            Q(services_offered__icontains=query) |
            Q(services__name__icontains=query)
        ).distinct()

    if category:
        providers = providers.filter(services__category__name=category).distinct()

    context = {
        'categories': categories,
        'providers': providers,
        'query': query,
        'selected_category': category,
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
<<<<<<< HEAD:searching/views.py
    return render(request, 'provider_detail.html', context)
=======
    return render(request, 'provider_detail.html', context)

@login_required
def seeker_dashboard(request):
    service_requests = ServiceRequest.objects.filter(seeker=request.user)
    return render(request, 'seeker_dashboard.html', {'service_requests': service_requests})

@login_required
def confirm_service(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    user = request.user

    # Seeker confirma
    if user == service_request.seeker:
        service_request.seeker_confirmed = True
    # Provider confirma
    elif hasattr(service_request, 'provider') and user == service_request.provider.user:
        service_request.provider_confirmed = True

    service_request.save()
    return redirect('seeker_dashboard')

@login_required
def provider_profile(request):
    provider, created = ServiceProvider.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, request.FILES, instance=provider)
        if form.is_valid():
            form.save()
            # Permanecer en la misma página después de guardar
            return redirect('provider_profile')
    else:
        form = ServiceProviderForm(instance=provider)
    return render(request, 'provider_profile.html', {'form': form, 'provider': provider})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crea el perfil de proveedor automáticamente
            from .models import ServiceProvider
            ServiceProvider.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
>>>>>>> c1cd290 (Avance chao):serconn_app/views.py
