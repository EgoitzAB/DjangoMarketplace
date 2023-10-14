# forms.py
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from .models import Order  # Import your Order model here

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'telefono',  # Match the field name in your model
            'city',
            'country',
            'line1',
            'line2',
            'postal_code',
            'provincia',
        ]


    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Agrega la lógica de verificación para el correo electrónico aquí
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Agrega la lógica de verificación adicional si es necesario
        return phone_number
