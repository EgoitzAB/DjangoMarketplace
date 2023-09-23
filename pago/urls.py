from django.urls import path
from django.conf import settings
from . import views

app_name = 'pago'

urlpatterns = [
    path('realizar-compra/', views.create_order, name='create_order'),
    path('confirmacion/<int:compra_id>/', views.confirmacion_compra, name='confirmacion'),
    path('get-buyers/', views.get_buyers, name='get-buyers'),
    path('prueba-order/', views.prueba_order, name='prueba_order'),
    #path('create-buyer/', views.create_buyer, name='create-buyer'),
]
