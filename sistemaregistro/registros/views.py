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
            # se guiarda el objeto en la base de datos
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
            # lo guarda y redirige a detalle registro
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