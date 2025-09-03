from django import forms
from .models import ServiceProvider

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = [
            'first_name', 'last_name', 'profession',
            'service_info', 'rates', 'availability', 'profile_picture',
            'contact_number', 'services_offered'
        ]

    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')
        if image:
            if image.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError("La imagen no debe superar los 2MB.")
        return image

