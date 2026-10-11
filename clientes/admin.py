from django.contrib import admin
from .models import Cliente,Visita

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display=["apellidos","nombre","sexo","edad","telefono","nutricionista","activo"]
    list_filter=["activo","sexo","nutricionista"]
    search_fields=["nombre","apellidos","telefono","email"]

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display=["cliente","numero","tipo","fecha","edad_cliente"]
    list_filter=["tipo"]
