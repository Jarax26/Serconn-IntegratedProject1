from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, ServiceProvider
from .forms import EditProfileForm, ServiceProviderForm
from interactions.models import Chat
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Tu cuenta se ha creado correctamente. Inicia sesión para continuar.")
            return redirect("login")
        else:
            pass
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "profile.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Redirección según rol
            if user.user_role == "service_seeker": # pyright: ignore[reportAttributeAccessIssue]
                return redirect("service_search")   # Vista buscador
            elif user.user_role == "service_provider": # pyright: ignore[reportAttributeAccessIssue]
                    return redirect("profile")  # Vista proveedor
            else:
                return redirect("service_search")  # fallback
        else:
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def provider_dashboard(request):
    provider, created = User.objects.get_or_create(id=request.user.id, defaults={'email': request.user.email})
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('provider_dashboard')
    else:
        form = CustomUserCreationForm(instance=provider)
    return render(request, 'provider_dashboard.html', {'form': form, 'provider': provider})

# @login_required
# def provider_profile(request):
#     provider, created = ServiceProvider.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = ServiceProviderForm(request.POST, request.FILES, instance=provider)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # recargar la página con los cambios guardados
#     else:
#         form = ServiceProviderForm(instance=provider)
#     return render(request, 'profile.html', {'form': form, 'provider': provider})


@login_required
def edit_profile_view(request):
    user = request.user
    service_provider = None

    if user.is_service_provider:  # solo si el usuario es proveedor
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

    return render(request, "edit_profile.html", {
        "form": user_form,
        "provider_form": provider_form
    })

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