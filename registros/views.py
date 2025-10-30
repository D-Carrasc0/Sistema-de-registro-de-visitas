from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro
from .forms import RegistroForm

# Create your views here.
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