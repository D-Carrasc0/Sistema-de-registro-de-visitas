from django.contrib import admin
from .models import Registro

# Register your models here.
admin.site.register(Registro)

# @admin.register(Registro) 
# class ProductoAdmin(admin.ModelAdmin): 
#     list_display = ("nombre", "rut", "motivo", "horaentrada","horasalida", "estado") 
#     search_fields = ("nombre", "rut")  # texto rápido 
#     list_filter = ("estado",)           # filtros laterales 
#     ordering = ("nombre",) 
#     list_per_page = 25 
#     autocomplete_fields = ()  # ej.: ("categoria",) si existiera FK grande 