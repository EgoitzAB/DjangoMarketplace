from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Order
from compra.carrito import Carrito
from .forms import OrderForm
import requests
from compra.context_processor import carrito_total
import logging  # Importa el módulo de registro de Django



def prueba_order(request):
    context = {}
    return render(request, 'pago/payindex.html', {'context': context})

def get_paygreen_jwt_token():
    url = "https://sb-api.paygreen.fr/auth/authentication/sh_1f13f081e35c460fbec63e876ea184e3/secret-key"
    headers = {"Authorization": "sk_b88a2138936d43839ac81686f7bbc2ea"}

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        jwt_token = response.json().get("data", {}).get("token")
        return jwt_token
    else:
        # Maneja el error si no se pudo obtener el token JWT
        return None

@login_required
def create_order(request):
    carrito = Carrito(request)
    precio_total = carrito.carrito_total()  # Define esta función para calcular el total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Guarda los datos del formulario en un nuevo objeto Order
            order = Order(
                usuario=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['phone_number'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
                line1=form.cleaned_data['line1'],
                line2=form.cleaned_data['line2'],
                postal_code=form.cleaned_data['postal_code'],
                state=form.cleaned_data['state'],
                total= precio_total,
            )

            # Resto de la lógica para enviar la orden a la API de PayGreen
            order.save()
            # Limpia el carrito después de la compra

            try:
                jwt_token = get_paygreen_jwt_token()
                print("Token JWT de PayGreen:", jwt_token)

                if jwt_token is not None:
                    buyer_url = "https://sb-api.paygreen.fr/payment/buyers"

                    buyer_data = {
                        "billing_address": {
                            "city": str(order.city),
                            "country": str(order.country),
                            "line1": str(order.line1),
                            "postal_code": str(order.postal_code)
                        },
                        "reference": f"r{order.id}",
                        "first_name": str(order.first_name),
                        "last_name": str(order.last_name),
                        "email": str(order.email),
                    }

                    headers = {
                       "accept": "application/json",
                       "content-type": "application/json",
                       "authorization": f"Bearer {jwt_token}"
                    }

                    buyer_response = requests.post(buyer_url, json=buyer_data, headers=headers)

                    buyer_response = requests.post(buyer_url, json=buyer_data, headers=headers)

                    # Check if the request was successful (status code 200)
                    if buyer_response.status_code == 200:
                        # Parse the JSON response
                        response_data = buyer_response.json()

                        # Access the 'data' key in the response_data dictionary
                        buy_id = response_data.get('data', {}).get('id')
                    else:
                        # Handle the case where the request was not successful
                        # You might want to log the error or return an appropriate response
                        return HttpResponse("Failed to create a buyer on PayGreen", status=buyer_response.status_code)


                    payload = {
                        "auto_capture": True,
                        "buyer": {
                            "billing_address": {
                                "city": f"{order.city}",
                                "country": f"{order.country}",
                                "line1": f"{order.line1}",
                                "postal_code": f"{order.postal_code}",
                                "state": f"{order.state}"
                            },
                            "id": f"r{order.id}", #aquí recuperar id del cliente
                            "reference": f"r{order.id}",
                            "first_name": f"{order.first_name}",
                            "last_name": f"{order.last_name}",
                            "email": f"{order.email}"
                        },
                        "currency": "eur",
                        "merchant_initiated": False,
                        "mode": "instant",
                        "partial_allowed": False,
                        "amount": 1000,
                        "description": "lote de productos",
                        "reference": f"r{order.id}",
                        "platforms": [
                            "bank_card"
                            ],
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
                        created_buyer = response.json()
                        print(created_buyer)
                        return render(request, 'pago/payindex.html', {'created_buyer': created_buyer})
                    else:
                        logging.error("Error al crear la compra en PayGreen: %s", response.text)
                        return render(request, 'pago/error.html', {'error_message': response.text})
                else:
                    return render(request, 'pago/error.html', {'error_message': "Error "})
            except requests.exceptions.RequestException as e:
                # Registra el error en el sistema de registro de Django
                logging.error("Error al realizar la solicitud a PayGreen: %s", str(e))
                return render(request, 'pago/error.html', {'error_message': str(e)})
    else:
        form = OrderForm()
        return render(request, 'pago/order_form.html', {'form': form})
    
    return render(request, 'pago/payindex.html', {'form': form, 'total': total})

@login_required
def confirmacion_compra(request, compra_id):
    compra = Order.objects.get(id=compra_id)
    return render(request, 'pago/confirmacion.html', {'compra': compra})



#necesito los datos del id y la secret key
def get_buyers(request):
    url = "https://api.paygreen.fr/payment/buyers"

    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción en caso de error HTTP
        buyers_data = response.json()
    except requests.exceptions.RequestException as e:
        buyers_data = {"error": str(e)}  # Maneja errores de solicitud

    return render(request, 'buyers_list.html', {'buyers_data': buyers_data})





