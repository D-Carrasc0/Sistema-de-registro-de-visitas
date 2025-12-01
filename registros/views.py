from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro
from .forms import RegistroForm

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils.timezone import localdate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import GroupSerializer, UserSerializer, RegistroSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # Todos los usuarios ordenador por fecha de union decendente
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    # Solo usuarios autenticados pueden acceder
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    # Todos los grupos ordenados alfabeticamentes
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    # Solo usuarios autenticados pueden acceder
    permission_classes = [permissions.IsAuthenticated]

class RegistroViewSet(viewsets.ModelViewSet):

    # Todos los registros ordenados por nombre
    queryset = Registro.objects.all().order_by('nombre')
    # Serializador
    serializer_class = RegistroSerializer
    # Solo usuarios autenticados pueden acceder
    permission_classes = [permissions.IsAuthenticated]  

# Indica que la vista solo puede recibir peticiones GET
@api_view(["GET"])
# Requiere que el usuario este autenticado
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    # Fecha actual (sin hora)
    hoy = localdate()
    # Calcula la fecha de hace 6 dias para tener un rango de 7 junto a hoy
    hace_7_dias = hoy - timedelta(days=6)

    # Métricas generales
    # Total de visitas (registros existentes)
    total_visitas = Registro.objects.count()
    # Registros cuya hora de entrada es hoy
    visitas_hoy = Registro.objects.filter(horaentrada__date=hoy).count()
    # Registros donde el estado_finalizado es false (no se ha terminado la visita)
    visitas_activas = Registro.objects.filter(estado_finalizado=False).count()

    # Visitas por día (últimos 7 días)
    visitas_por_dia_qs = (
        Registro.objects
        # Filtra los registros que su hora_entrada este en los ultimos 7 dias
        .filter(horaentrada__date__gte=hace_7_dias)
        # Trunca horaentrada a solo fecha para agrupar por dia
        .annotate(dia=TruncDate("horaentrada"))
        # Selecciona solo el campo dia
        .values("dia")
        # Cuenta cuantos registros hay por dia
        .annotate(total=Count("id"))
        # Ordena cronologicamente por dia
        .order_by("dia")
    )

    # Convierte la query en un diccionario
    visitas_por_dia = [
        {
            #Convierte la fecha en un string con formato "YYYY-MM-DD"
            "dia": v["dia"].strftime("%Y-%m-%d"), 
            "total": v["total"],
        }
        for v in visitas_por_dia_qs
    ]

    # Visitas finalizadas vs incompletas
    # Calcula cuantas visitas han sido finalizados con cuales no usando filtros en count
    estados = Registro.objects.aggregate(
        finalizadas=Count("id", filter=Q(estado_finalizado=True)),
        incompletas=Count("id", filter=Q(estado_finalizado=False)),
    )

    # Retorna los datos en formato JSON
    return Response({
        "total_visitas": total_visitas,
        "visitas_hoy": visitas_hoy,
        "visitas_activas": visitas_activas,
        "visitas_por_dia": visitas_por_dia,
        "estados": estados,
    })

# Vistas 

def lista_registros(request):
    # obtiene todos los objetos del modelo registro de la base de datos
    registros = Registro.objects.all()
    return render(request, 'registros/lista_registros.html', {'registros': registros})

def detalle_registro(request, pk):
    # obtiene la pk (llave primaria) del registro y si no la obtiene devuelve un error 404
    registro = get_object_or_404(Registro, pk=pk)
    return render(request, 'registros/detalle_registro.html', {'registro': registro})   

def nuevo_registro(request):
    # si el metodo es POST osea se hizo un submit
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        # si los datos son validos
        if form.is_valid():
            # con cleaned_data accedemos a los datos limpios despues de la validacion estos vienen en formato de diccionario
            fecha_entrada = form.cleaned_data['horaentrada']
            fecha_salida = form.cleaned_data['horasalida']
            estado_finalizado = form.cleaned_data['estado_finalizado']

            # si existe fecha entrada y no de salida y se marca la visita como finalizada da un error
            if fecha_entrada and estado_finalizado and not fecha_salida and estado_finalizado == True:
                form.add_error('estado_finalizado', 'para marcar estado finalizado debe estar la fecha de entrada y salida')
            elif fecha_entrada and fecha_salida and estado_finalizado == False:
                form.add_error('estado_finalizado', 'Si finalizo la visita marque la casilla')
            # si existe la fecha de entrada y salida ademas de si la fecha de entrada es mayor o igual a la de salida
            elif fecha_entrada and fecha_salida and fecha_entrada >= fecha_salida:
                # el formulario desplegara un error en el campo horasalida con el mensaje
                form.add_error('horasalida', 'la hora de salida debe ser despues de la entrada')
            # se guarda el objeto en la base de datos
            else:
                form.save()
                return redirect('lista_registros')
    else:
        form = RegistroForm()
    return render(request, 'registros/nuevo_registro.html', {'form': form})

def editar_registro(request, pk):
    # obtiene la pk (llave primaria) del registro y si no la obtiene devuelve un error 404
    registro = get_object_or_404(Registro, pk=pk)
    if request.method == 'POST':
        # intenta guardar los cambios 
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            # con cleaned_data accedemos a los datos limpios despues de la validacion estos vienen en formato de diccionario
            fecha_entrada = form.cleaned_data['horaentrada']
            fecha_salida = form.cleaned_data['horasalida']
            estado_finalizado = form.cleaned_data['estado_finalizado']

            # si existe fecha entrada y no de salida y se marca la visita como finalizada da un error
            if fecha_entrada and estado_finalizado and not fecha_salida and estado_finalizado == True:
                form.add_error('estado_finalizado', 'para marcar estado finalizado debe estar la fecha de entrada y salida')
            elif fecha_entrada and fecha_salida and estado_finalizado == False:
                form.add_error('estado_finalizado', 'Si finalizo la visita marque la casilla')
            # si existe la fecha de entrada y salida ademas de si la fecha de entrada es mayor o igual a la de salida
            elif fecha_entrada and fecha_salida and fecha_entrada >= fecha_salida:
                # el formulario desplegara un error en el campo horasalida con el mensaje
                form.add_error('horasalida', 'la hora de salida debe ser despues de la entrada')
            # lo guarda y redirige a detalle registro
            else:
                form.save()
                return redirect('detalle_registro', pk=registro.pk)
    else:
        form = RegistroForm(instance=registro)
    return render(request, 'registros/editar_registro.html', {'form': form})    

def eliminar_registro(request, pk):
    # obtiene la pk (llave primaria) del registro y si no la obtiene devuelve un error 404
    registro = get_object_or_404(Registro, pk=pk)
    if request.method == 'POST':
        # elimina el registro y redirige a la lista con los registros
        registro.delete()
        return redirect('lista_registros')
    return render(request, 'registros/eliminar_registro.html', {'registro': registro})  