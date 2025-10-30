from django.contrib import admin
from .models import Registro
from django.utils import timezone

# Register your models here.
@admin.action(description="Marcar salidas como completas")
def marcar_salidas(modeladmin, request, queryset):
    # Obtener la hora actual para la hora de salida
    hora_actual = timezone.now()

    # Actualizar las visitas seleccionadas
    updated = queryset.update(estado_finalizado=True, horasalida=hora_actual)

    # Mostrar mensaje de confirmación
    modeladmin.message_user(request, f"{updated} visitas han sido marcadas como completas.")

@admin.register(Registro) 
class ProductoAdmin(admin.ModelAdmin): 
    list_display = ("nombre", "rut", "motivo", "horaentrada","horasalida", "estado_finalizado") 
    search_fields = ("nombre", "rut")  # texto rápido 
    list_filter = ("horaentrada", "horasalida")           # filtros laterales 
    ordering = ("nombre",) 
    list_per_page = 25 
    actions = [marcar_salidas]