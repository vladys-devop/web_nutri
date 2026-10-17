from django.urls import path

from . import views

urlpatterns = [
    path("", views.cliente_lista, name="cliente_lista"),
]
