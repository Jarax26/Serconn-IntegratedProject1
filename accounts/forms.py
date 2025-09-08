from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ServiceProvider

class CustomUserCreationForm(UserCreationForm):
    description = forms.CharField(
        required=True,  # Solo obligatorio para service_provider
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "placeholder": "Descripción personal (incluye habilidades, experiencia, etc...)"}),
        label="Descripción personal",
    )

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "user_birthdate", "user_city", "user_address",
            "user_phone", "email", "password1", "password2", "description",
            "user_role", "user_picture"
        ]
        widgets = {
            "user_birthdate": forms.DateInput(attrs={"type": "date"}),
            "user_picture": forms.ClearableFileInput(attrs={
                "id": "id_user_picture",              
                "accept": "image/*",
                "class": "block w-full text-sm text-gray-600 cursor-pointer "
                         "file:mr-4 file:py-2 file:px-4 "
                         "file:rounded-full file:border-0 "
                         "file:text-sm file:font-semibold "
                         "file:bg-indigo-50 file:text-indigo-700 "
                         "hover:file:bg-indigo-100"
            })
        }
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "user_birthdate": "Fecha de Nacimiento",
            "user_city": "Ciudad",
            "user_address": "Dirección",
            "user_phone": "Teléfono",
            "email": "Correo Electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar Contraseña",
            "user_role": "Tipo de Usuario",
            "user_picture": "Foto de Perfil",
        }

    def clean_user_picture(self):
        image = self.cleaned_data.get("user_picture")
        if not image:
            raise forms.ValidationError("Debes subir una foto de perfil.")
        if image.size > 2 * 1024 * 1024:  # 2MB
            raise forms.ValidationError("La imagen no debe superar los 2MB.")
        return image

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.user_role == "service_provider":
                ServiceProvider.objects.create(
                    user=user,
                    description=self.cleaned_data.get("description", "")
                )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["user_picture"].required = True
        data = self.data or getattr(self, 'initial', {})
        role = data.get("user_role") or self.initial.get("user_role")
        if role == "service_provider":
            self.fields["description"].required = True
        else:
            self.fields["description"].required = False

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "border rounded-lg p-2 w-full", "rows": 4}),
        }
        labels = {
            "description": "Descripción",
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "user_city", "user_address",  "user_phone", "user_picture"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "last_name": forms.TextInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "email": forms.EmailInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "user_city": forms.Select(attrs={"class": "border rounded-lg p-2 w-full"}),
            "user_address": forms.TextInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "user_phone": forms.TextInput(attrs={"class": "border rounded-lg p-2 w-full"}),
            "user_picture": forms.ClearableFileInput(attrs={"class": "border rounded-lg p-2 w-full"}),
        }
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "user_city": "Ciudad",
            "user_address": "Dirección",
            "user_phone": "Teléfono",
            "email": "Correo Electrónico",
            "user_picture": "Foto de Perfil",
        }

