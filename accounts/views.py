from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


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
                return redirect("provider_dashboard")  # Vista proveedor
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
