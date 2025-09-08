from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'rate']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ej: Clases de matemáticas'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe brevemente el servicio'}),
            'rate': forms.NumberInput(attrs={'placeholder': 'Ej: 50000'}),
        }
