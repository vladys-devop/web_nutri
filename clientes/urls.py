from django.urls import path

from . import views

urlpatterns = [
    path("", views.cliente_lista, name="cliente_lista"),
    path("<int:pk>/", views.cliente_detalle, name="cliente_detalle"),
]
