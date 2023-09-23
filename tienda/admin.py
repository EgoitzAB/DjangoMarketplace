from django.contrib import admin
from .models import Producto, Precio_stock

# Register your models here.
class PreciosInLine(admin.TabularInline):
    model = Precio_stock
    extra = 1

class ProductoAdmin(admin.ModelAdmin):

    def get_precios(self, obj):
        precios = obj.precios.all()
        return ", ".join(str(p.precio) for p in precios) if precios.exists() else None

    get_precios.short_description = "Precios"
    list_display = ("name", "get_precios", "categoria",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PreciosInLine]

admin.site.register(Producto, ProductoAdmin)