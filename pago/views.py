from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.transaction import atomic, non_atomic_requests 
from .models import Order, PaygreenWebhookMessage
from tienda.models import Precio_stock
from compra.carrito import Carrito
from .forms import OrderForm
import requests
from compra.context_processor import carrito_total
import logging
import json
import datetime as dt
from secrets import compare_digest
from allauth.account.decorators import verified_email_required
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone


def prueba_order(request):
    context = {}
    return render(request, 'pago/payindex.html', {'context': context})

def get_paygreen_jwt_token():
    """ Obtener el token de pago """
    url = "https://sb-api.paygreen.fr/auth/authentication/sh_1f13f081e35c460fbec63e876ea184e3/secret-key"
    headers = {"Authorization": "sk_b88a2138936d43839ac81686f7bbc2ea"}

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        jwt_token = response.json().get("data", {}).get("token")
        return jwt_token
    else:
        return None

def create_buyer(jwt, order):
    buyer_url = "https://sb-api.paygreen.fr/payment/buyers"
    buyer_data = {
                "billing_address": {
                "city": str(order.city),
                "country": str(order.country),
                "line1": str(order.line1),
                "postal_code": str(order.postal_code),
                "state": str(order.provincia)
                 },
                "reference": f"{order.first_name} {order.last_name} / {order.email} {order.id}",
                "first_name": str(order.first_name),
                "last_name": str(order.last_name),
                "email": str(order.email),
                "phone_number": str(order.telefono),
                }

    headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {jwt}"
            }

    buyer_response = requests.post(buyer_url, json=buyer_data, headers=headers)
    if buyer_response.status_code == 200:
        response_data = buyer_response.json()
        buy_id = response_data.get('data', {}).get('id')
        return buy_id
    else:
        return HttpResponse("Failed to create a buyer on PayGreen", status=buyer_response.status_code)

@verified_email_required
@login_required
def create_order(request):
    """ Crear la orden y manejar la redirección a la página de pago y la vuelta """
    carrito = Carrito(request)
    precio_total = carrito.carrito_total()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid() and precio_total > 0:
            order = Order(
                usuario=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
                line1=form.cleaned_data['line1'],
                line2=form.cleaned_data['line2'],
                postal_code=form.cleaned_data['postal_code'],
                provincia=form.cleaned_data['provincia'],
                total= precio_total,
            )
            order.save()
        
            
            try:
                jwt_token = get_paygreen_jwt_token()
                print("Token JWT de PayGreen:", jwt_token)
                if jwt_token is not None:
                    buy_id = create_buyer(jwt_token, order)
                    
                    payload = {
                        "auto_capture": True,
                        "buyer": buy_id,
                        "currency": "eur",
                        "merchant_initiated": False,
                        "mode": "instant",
                        "partial_allowed": False,
                        "amount": order.total,
                        "description": f"Lote de productos {order.id} LRVCBD",
                        "integration_mode": "hosted_fields",
                        "description": "lote de productos",
                        "reference": f"r{order.id}",
                        "return_url": request.build_absolute_uri(reverse('pago:confirmacion', args=[order.id])),
                        "cancel_url": request.build_absolute_uri(reverse('pago:cancelacion', args=[order.id])),
                        "shop_id": "sh_1f13f081e35c460fbec63e876ea184e3"
                    }

                    headers = {
                        "accept": "application/json",
                        "content-type": "application/json",
                        "authorization": f"Bearer {jwt_token}"
                    }
                
                    paygreen_url = "https://sb-api.paygreen.fr/payment/payment-orders"
                    response = requests.post(paygreen_url, json=payload, headers=headers)

                    if response.status_code == 200:
                        created_order = response.json()
                        print(created_order)
                        hosted_payment_url = created_order['data']['hosted_payment_url']
                        request.session.set_expiry(60)
                        with atomic():  # Iniciar una transacción
                            for producto_number, detalles in carrito.carrito.items():
                                producto_id = detalles['producto_id']  # Aquí puedes acceder al objeto Producto si lo necesitas
                                cantidad = detalles['quantity']
                                
                                try:
                                    producto = Precio_stock.objects.get(pk=producto_id)  # Obtiene el objeto Producto correspondiente
                                except Precio_stock.DoesNotExist:
                                    logging.error("El producto no existe.")
                                    continue

                                # Reducir la cantidad en stock del producto
                                if producto.stock >= cantidad:
                                    producto.stock -= cantidad
                                    producto.save()
                                else:
                                    # Manejar la situación donde el stock no es suficiente (puede lanzar una excepción o notificar al usuario)
                                    continue
                            
                        return redirect(hosted_payment_url)                     
                    else:
                        logging.error("Error al crear la compra en PayGreen: %s", response.text)
                        return render(request, 'pago/cancelacion.html')
                else:
                    return render(request, 'pago/error.html', {'error_message': "Error "})
            except requests.exceptions.RequestException as e:
                # Registra el error en el sistema de registro de Django
                logging.error("Error al realizar la solicitud a PayGreen: %s", str(e))
                return render(request, 'pago/error.html', {'error_message': str(e)})
        else:
            logging.error("El precio total del carrito es menor o igual a cero.")
            return redirect(reverse('compra:carrito'))
    else:
        form = OrderForm()
        return render(request, 'pago/order_form.html', {'form': form})
    

@login_required
def confirmacion_compra(request, compra_id):
    compra = Order.objects.get(id=compra_id)
    return render(request, 'pago/confirmacion.html', {'compra': compra})

@login_required
def cancelacion_compra(request, compra_id):
    compra = Order.objects.get(id=compra_id)
    return render(request, 'pago/cancelacion.html', {'compra': compra})


@csrf_exempt
@require_POST
@non_atomic_requests
def paygreen_webhook(request):
    given_token = request.headers.get("Paygreen-Webhook-Token", "")
    if not compare_digest(given_token, settings.PAYGREEN_WEBHOOK_TOKEN):
        return HttpResponseForbidden(
            "Incorrect token in Paygreen-Webhook-Token header.",
            content_type="text/plain",
        )

    PaygreenWebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=7)
    ).delete()
    payload = json.loads(request.body)
    PaygreenWebhookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    process_webhook_payload(payload)
    return HttpResponse("Message received okay.", content_type="text/plain")

@atomic
def process_webhook_payload(payload):
    pass




