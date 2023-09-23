# forms.py
from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from .models import Order

User = get_user_model()

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone_number = PhoneNumberField()
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    line1 = forms.CharField(max_length=255)
    line2 = forms.CharField(max_length=255, required=False)
    postal_code = forms.CharField(max_length=10)
    state = forms.CharField(max_length=100, required=False)

    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        # Agrega la lógica de verificación para la referencia aquí (por ejemplo, verifica si la orden o el usuario existe)
        return reference

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Agrega la lógica de verificación para el correo electrónico aquí
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Agrega la lógica de verificación para el número de teléfono aquí
        return phone_number
