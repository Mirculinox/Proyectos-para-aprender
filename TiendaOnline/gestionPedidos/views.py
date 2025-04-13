from django.shortcuts import render
from django.http import HttpResponse
from gestionPedidos.models import Articulos
from gestionPedidos.forms import FormularioContacto

# Create your views here.

def busqueda_productos (request):
    return render(request, "busqueda_productos.html")

def buscar(request):
    if request.GET["prd"]:
        #mensaje="Artículo buscado: %r" %request.GET["prd"]
        producto=request.GET["prd"]
        if len(producto)>20:
            mensaje= "Texto de búsqueda demasiado largo"
        else:
            articulos=Articulos.objects.filter(nombre__icontains= producto)
            return render(request, "resultados_busqueda.html", {"articulos":articulos, "query":producto})

    else:
        mensaje="No has introducido nada"

    return HttpResponse(mensaje)

def contacto (request):
    if request.method=='POST':
        #return render(request, "gracias.html")
        miFormulario=FormularioContacto(request.POST)
        
        if miFormulario.is_valid():
            information=miFormulario.cleaned_data

            send_mail(information['asunto'], information['mensaje'], information.get('email',''), ["miguelhgoico@gmail.com"],)
            
            return render(request, "gracias.html")
    else:

        miFormulario=FormularioContacto()
        return render(request, "formulario_contacto.html", {"form":miFormulario})