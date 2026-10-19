from django.urls import path

from . import views

urlpatterns = [
    path("", views.cliente_lista, name="cliente_lista"),
    path("nou/", views.cliente_nuevo, name="cliente_nuevo"),
    path("<int:pk>/", views.cliente_detalle, name="cliente_detalle"),
    path("<int:pk>/editar/", views.cliente_editar, name="cliente_editar"),
    path("<int:pk>/primera-visita/", views.primera_visita, name="primera_visita"),
]
