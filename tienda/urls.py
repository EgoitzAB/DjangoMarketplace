from django.urls import path
from .views import PrincipalView, CategoriasView, ProductoDetailView
from django.views.generic.base import RedirectView
from django.templatetags.static import static

app_name = "tienda"

urlpatterns = [
    path('', PrincipalView.as_view(), name="home"),
    path('productos/', CategoriasView.as_view(), name='listado'),
    path('productos/<slug:slug>/', ProductoDetailView.as_view(), name='detalle'),
    path('favicon.ico',RedirectView.as_view(url=static('favicon.ico'))),
]