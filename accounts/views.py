from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, EditProfileForm, ServiceProviderForm, AvailabilityForm
from .models import User, ServiceProvider, Availability
from interactions.models import Chat
from django.http import JsonResponse
from django.urls import reverse
import json

def register(request):
    # Si la petición es POST, la manejamos como una validación AJAX
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Aunque no se mostrará de inmediato, es bueno dejar el mensaje para la sesión
            messages.success(request, "Tu cuenta se ha creado correctamente. Inicia sesión para continuar.")
            
            # Construye la URL de login para la redirección en el frontend
            login_url = reverse('login')
            return JsonResponse({'status': 'success', 'redirect_url': login_url})
        else:
            # Si el formulario no es válido, devuelve los errores como JSON
            # json.loads convierte el string de errores de Django a un diccionario real
            return JsonResponse({'status': 'error', 'errors': json.loads(form.errors.as_json())})

    # Si la petición es GET, simplemente muestra el formulario vacío
    else:
        form = CustomUserCreationForm()
    
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_role == "service_seeker":
                return redirect("service_search")
            elif user.user_role == "service_provider":
                return redirect("profile")
            else:
                return redirect("service_search")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def edit_profile_view(request):
    user = request.user
    service_provider = None
    if user.is_service_provider:
        service_provider, _ = ServiceProvider.objects.get_or_create(user=user)
    if request.method == "POST":
        user_form = EditProfileForm(request.POST, request.FILES, instance=user)
        provider_form = ServiceProviderForm(request.POST, instance=service_provider) if service_provider else None
        if user_form.is_valid() and (provider_form is None or provider_form.is_valid()):
            user_form.save()
            if provider_form:
                provider_form.save()
            return redirect("profile")
    else:
        user_form = EditProfileForm(instance=user)
        provider_form = ServiceProviderForm(instance=service_provider) if service_provider else None
    return render(request, "edit_profile.html", {"form": user_form, "provider_form": provider_form})


@login_required
def profile_view(request):
    chats = None
    if request.user.is_service_provider:
        chats = Chat.objects.filter(provider=request.user)
    return render(request, "profile.html", {"chats": chats})


@login_required
def user_profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile.html', {'profile_user': profile_user})


@login_required
def availability_view(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.provider = provider
            availability.save()
            messages.success(request, "Nuevo horario de disponibilidad añadido.")
            return redirect('availability')
    else:
        form = AvailabilityForm()
    
    availabilities = Availability.objects.filter(provider=provider).order_by('start_time')
    return render(request, 'availability.html', {'form': form, 'availabilities': availabilities})


@login_required
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id)

    if availability.provider.user != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este horario.")

    if request.method == 'POST':
        availability.delete()
        messages.success(request, "Horario de disponibilidad eliminado correctamente.")
    
    return redirect('availability')