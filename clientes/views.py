from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.db.models import Q 



@login_required
def inicio(request):
    return render(request, "clientes/inicio.html")

@login_required
def cliente_lista(request):
    clientes = request.user.clientes.filter(activo=True)

    q = request.GET.get("q","").strip()
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q)
            | Q(apellidos__icontains=q)
            | Q(telefono__icontains=q)
        )

    return render(request, "clientes/lista.html", {
        "clientes" : clientes,
        "q" : q, 
    })

@login_required
def cliente_detalle(request, pk):
    cliente = get_object_or_404(request.user.clientes, pk=pk)

    return render(request, "clientes/detalle.html", {
        "cliente" : cliente,
    })