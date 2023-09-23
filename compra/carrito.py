from tienda.models import Precio_stock

class Carrito:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto):
        stock_precio = producto # PRECIO_STOCK.OBJECT
        producto = producto.producto # PRECIO_STOCK.OBJECT.PRODUCTO DEVUELVE MÉTODO __STR__ DE MODELO PRODUCTO
        id = str(stock_precio.id) # DEVUELVE EL ID DEL MODELO PRODUCTO
        if id not in self.carrito.keys():

            self.carrito[id] = {
                #'userid': self.request.user.id,
                'producto_id': stock_precio.id,
                'name': producto.name,
                'quantity': 1,
                'precio': stock_precio.precio,
                'stock': stock_precio.stock,
                'foto': producto.fotos.url,
                'link': producto.slug,
            }
        else:
            for key, value in self.carrito.items():
                if key == id:
                    value["quantity"] = value["quantity"] + 1
                    break
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def restar(self, producto):
        producto = producto
        id = str(producto.id)
        if id in self.carrito:
            if self.carrito[id]['quantity'] > 1:
                self.carrito[id]['quantity'] -= 1
            else:
                del self.carrito[id]
            self.guardar_carrito()

    def eliminar(self, producto):
        producto = producto
        id = str(producto.id)
        if id in self.carrito:
            if self.carrito[id]['quantity'] > 0:
                del self.carrito[id]
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
    
    def obtener_cantidad_producto(self, producto_id):
        """
        Obtiene la cantidad de un producto específico en el carrito.
        """
        id = str(producto_id)
        if id in self.carrito:
            return self.carrito[id]['quantity']
        return 0
    
    def calcular_total(self):
        total = 0
        for producto_id, detalles in self.carrito.items():
            total += detalles['precio'] * detalles['quantity']
        return total
    
    def carrito_total(self):
        total_carrito = 0
        for key, value in self.carrito.items():
            total_carrito = total_carrito + value['precio'] * value['quantity']
        return total_carrito
