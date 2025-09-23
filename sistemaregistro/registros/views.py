from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro
from .forms import RegistroForm

# Create your views here.
def lista_registros(request):
    registros = Registro.objects.all()
    return render(request, 'registros/lista_registros.html', {'registros': registros})

def detalle_registro(request, pk):
    registro = get_object_or_404(Registro, pk=pk)
    return render(request, 'registros/detalle_registro.html', {'registro': registro})   

def nuevo_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_registros')
    else:
        form = RegistroForm()
    return render(request, 'registros/nuevo_registro.html', {'form': form})

def editar_registro(request, pk):
    registro = get_object_or_404(Registro, pk=pk)
    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('detalle_registro', pk=registro.pk)
    else:
        form = RegistroForm(instance=registro)
    return render(request, 'registros/editar_registro.html', {'form': form})    

def eliminar_registro(request, pk):
    registro = get_object_or_404(Registro, pk=pk)
    if request.method == 'POST':
        registro.delete()
        return redirect('lista_registros')
    return render(request, 'registros/eliminar_registro.html', {'registro': registro})  