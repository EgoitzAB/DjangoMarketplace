from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from tienda.models import Producto

User = get_user_model()

class Order(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cliente')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = PhoneNumberField(null=False, blank=False)

    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100, null=True, blank=True)

    productos = models.ManyToManyField(Producto)
    total = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Compra {self.id}"
    
class ArchivedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = PhoneNumberField(unique=True, null=False, blank=False)

    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100, null=True, blank=True)

    productos = models.ManyToManyField(Producto)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Archived User: {self.user.username} ({self.user.id})"
