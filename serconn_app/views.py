from django.shortcuts import render, get_object_or_404
from .models import ServiceProvider, ServiceCategory, Service
from django.http import Http404

# Vistas para la sección de búsqueda y perfiles
def service_search_view(request):
    """
    Vista principal para la búsqueda de servicios.
    """
    # Obtener todas las categorías de servicio para el menú desplegable
    categories = ServiceCategory.objects.all()
    
    # Inicializar la lista de proveedores
    providers = ServiceProvider.objects.all()
    query = None
    category = None
   
    # Procesar la búsqueda por palabra clave
    if 'query' in request.GET:
        query = request.GET['query']
        # Buscar en los campos del modelo que coincidan con la palabra clave
        providers = providers.filter(description__icontains=query)

    # Procesar el filtro por categoría
    if 'category' in request.GET and request.GET['category']:
        category = request.GET['category']
        # Asumiendo una relación ManyToMany entre ServiceProvider y ServiceCategory
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
