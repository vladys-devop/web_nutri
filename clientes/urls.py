from django.urls import path

from . import views

urlpatterns = [
    path("", views.cliente_lista, name="cliente_lista"),
    path("nou/", views.cliente_nuevo, name="cliente_nuevo"),
    path("<int:pk>/", views.cliente_detalle, name="cliente_detalle"),
]
