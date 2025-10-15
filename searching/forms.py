from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'rate']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ej: Clases de matemáticas',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe brevemente el servicio',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'rows': 4
            }),
            'rate': forms.NumberInput(attrs={
                'placeholder': 'Ej: 50000',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500'
            }),
        }