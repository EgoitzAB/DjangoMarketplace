from django.db import models
import os
import uuid
# Create your models here.
def productos_directory_path(instance, filename):
    unique_filename = str(uuid.uuid4())
    ext = filename.split('.')[-1]
    safe_directory_name = instance.name.replace(" ", "_").lower()
    full_path = os.path.join('productos', safe_directory_name, unique_filename + '.' + ext)
    return full_path


class Producto(models.Model):
    CATEGORIAS = (
        ('COSMÉTICOS', 'Cosméticos'),
        ('FLORES', 'Flores'),
        ('ROPA', 'Ropa'),
        ('COMESTIBLES', 'Comestibles'),
        ('VARIOS', 'Varios'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    fotos = models.ImageField(blank=True, null=True, upload_to=productos_directory_path)
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default="FLORES")

    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Precio_stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="precios")
    precio = models.PositiveSmallIntegerField(blank=True, null=True)
    peso = models.PositiveSmallIntegerField(blank=True, null=True)
    stock = models.PositiveIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True, unique=True)