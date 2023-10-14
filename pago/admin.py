from django.contrib import admin
from django import forms
from .models import Order
from .forms import OrderForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class ContactForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='ES'),
        }

@admin.register(Order)
class ContactAdmin(admin.ModelAdmin):
    form = OrderForm