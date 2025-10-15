# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date
from .models import User, ServiceProvider, Availability

class CustomUserCreationForm(UserCreationForm):
    """
    Un formulario de creación de usuario personalizado con validaciones estrictas
    y campos adicionales para el registro en SERCONN.
    """
    # === Campos Adicionales que no están en el modelo base de User ===
    
    # Campo para el rol del usuario, con un widget de input oculto
    user_role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.HiddenInput(),
        label="Tipo de Usuario"
    )
    user_city = forms.ChoiceField(
        choices=User.CITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-secondary focus:border-transparent transition'
        })
    )
    # Campos del perfil del usuario
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    user_birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Fecha de Nacimiento")
    user_city = forms.ChoiceField(choices=User.CITY_CHOICES, required=True, label="Ciudad")
    user_address = forms.CharField(max_length=100, required=True, label="Dirección")
    user_phone = forms.CharField(max_length=20, required=True, label="Teléfono")
    user_picture = forms.ImageField(required=True, label="Foto de Perfil")
    
    # Campo específico para proveedores
    description = forms.CharField(
        required=False, # La obligatoriedad se maneja en __init__
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Describe tu experiencia, habilidades y lo que te hace un gran proveedor..."}),
        label="Descripción Profesional"
    )

    class Meta:
        model = User
        fields = ("email",)
        
    def __init__(self, *args, **kwargs):
        """
        Constructor para aplicar clases CSS y lógica condicional a los campos.
        """
        super().__init__(*args, **kwargs)
        
        # Define el orden de los campos como aparecerán en el formulario
        self.order_fields([
            'first_name', 'last_name', 'user_birthdate', 'user_city', 'user_address',
            'user_phone', 'email', 'password1', 'password2', 'user_picture', 'description', 'user_role'
        ])

        # Aplica clases de Tailwind a todos los campos para una apariencia consistente
        common_classes = 'w-full p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-secondary focus:border-transparent transition'
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput, forms.DateInput, forms.ChoiceField, forms.Textarea)):
                field.widget.attrs.update({'class': common_classes})
        
        self.fields['user_picture'].widget.attrs.update({
            'class': 'block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-brand-secondary/10 file:text-brand-secondary hover:file:bg-brand-secondary/20 cursor-pointer'
        })
        
        # Ayuda contextual para el campo de contraseña
        self.fields['password1'].help_text = 'Usa 8+ caracteres, con una mezcla de letras, números y símbolos.'

        # Lógica para hacer 'description' requerida solo si el rol es proveedor
        # Usamos `self.data` para obtener los datos del POST
        if 'user_role' in self.data and self.data.get('user_role') == 'service_provider':
            self.fields['description'].required = True

    # === Métodos de Validación Específicos ('clean_<field_name>') ===

    def clean_user_phone(self):
        """
        Valida que el teléfono contenga solo dígitos y tenga una longitud mínima de 7.
        """
        phone = self.cleaned_data.get('user_phone')
        if phone and not phone.isdigit():
            raise ValidationError("El número de teléfono debe contener solo dígitos.", code='invalid_phone_format')
        if phone and len(phone) < 7:
            raise ValidationError("El número de teléfono debe tener al menos 7 dígitos.", code='invalid_phone_length')
        return phone

    def clean_user_birthdate(self):
        """
        Valida que el usuario sea mayor de 18 años y la fecha no sea en el futuro.
        """
        birthdate = self.cleaned_data.get('user_birthdate')
        if not birthdate:
            return birthdate # La validación 'required' se encarga de esto.

        today = date.today()
        if birthdate > today:
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.", code='future_date')

        age = (today - birthdate).days / 365.25
        if age < 18:
            raise ValidationError("Debes ser mayor de 18 años para registrarte.", code='underage')
        if age > 100:
            raise ValidationError("Por favor, ingresa una fecha de nacimiento válida.", code='unrealistic_age')
        
        return birthdate

    def clean_user_picture(self):
        """
        Valida que se haya subido una imagen y que no exceda el tamaño máximo de 2MB.
        """
        image = self.cleaned_data.get("user_picture", False)
        if not image:
            # Esta validación se maneja con `required=True` en la definición del campo.
            return image
        if image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("La imagen no debe superar los 2MB.", code='image_too_large')
        return image

    def save(self, commit=True):
        """
        Guarda el objeto User y, si es un proveedor, su perfil de ServiceProvider asociado.
        """
        user = super().save(commit=False)
        
        # Asignar todos los datos del formulario al objeto de usuario
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_role = self.cleaned_data['user_role']
        user.user_city = self.cleaned_data['user_city']
        user.user_address = self.cleaned_data['user_address']
        user.user_phone = self.cleaned_data['user_phone']
        user.user_birthdate = self.cleaned_data['user_birthdate']
        user.user_picture = self.cleaned_data['user_picture']
        
        if commit:
            user.save()
            if user.user_role == 'service_provider':
                ServiceProvider.objects.create(
                    user=user,
                    description=self.cleaned_data.get('description', '')
                )
        return user
    
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

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }