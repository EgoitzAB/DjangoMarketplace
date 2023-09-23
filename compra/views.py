from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from tienda.models import Producto, Precio_stock
from django.http.response import JsonResponse
from django.urls import reverse
from django.conf import settings
from compra.carrito import Carrito

# Create your views here.
def carrito(request):
    carrito = Carrito(request)
    return render(request, "compra/carrito.html", {"carrito": carrito})

def agregar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        carrito = Carrito(request)
        producto = Precio_stock.objects.get(id=producto_id)
        carrito.agregar(producto)
        return redirect("compra:carrito")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Precio_stock.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("compra:carrito")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Precio_stock.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("compra:carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("compra:carrito")