from django.contrib import admin
from gestionPedidos.models import Clientes, Articulos, Pedidos

# Register your models here.

class ClientesAdmin(admin.ModelAdmin):
    list_display=("nombre", "email", "tlfno",)
    search_fields=("nombre", "tlfno",)

class ArticulosAdmin(admin.ModelAdmin):
    list_display= ('nombre',)
    list_filter= ('seccion',)

class PedidosAdmin(admin.ModelAdmin):
    list_display= ("numero", "fecha",)
    list_filter=('fecha',)
    date_hierarchy='fecha'

admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(Pedidos, PedidosAdmin)

