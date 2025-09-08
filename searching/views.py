from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceCategory, Service
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from accounts.models import ServiceProvider
from .forms import ServiceForm


@login_required
def service_search_view(request):
    """
    Vista principal para la búsqueda de servicios.
    """
    categories = ServiceCategory.objects.all()
    
    # Solo proveedores con al menos un servicio
    providers = ServiceProvider.objects.select_related("user").filter(services__isnull=False).distinct()
    
    query = request.GET.get('query')
    category = request.GET.get('category')

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
    return render(request, 'provider_detail.html', context)

@login_required
def seeker_dashboard(request):
    service_requests = ServiceRequest.objects.filter(seeker=request.user)
    return render(request, 'seeker_dashboard.html', {'service_requests': service_requests})

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
