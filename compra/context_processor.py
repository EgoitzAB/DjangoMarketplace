from .carrito import Carrito

def carrito_total(request):
    carrito = Carrito(request)
    total_carrito = 0
    for key, value in carrito.carrito.items():
        total_carrito = total_carrito + value['precio'] * value['quantity']
    return {'carrito_total': total_carrito}