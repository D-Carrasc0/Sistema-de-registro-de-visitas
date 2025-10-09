from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        # campos del formulario
        fields = ['nombre', 'rut', 'motivo', 'horaentrada', 'horasalida']
        # configuracion de widgets para definir como se muestran los inputs
        widgets = {
            # en el campo rut se coloco un placeholder y un pattern (patron) para validar el formato
            # primero acepta un numero del 1 al 9 y despues entre 6-7 numeros entre el 0-9 despues un guion para finalmente aceptar un numero 0-9 ademas de K-k
            'rut': forms.TextInput(
                attrs={'placeholder': "12345678-9", 'pattern': "^[1-9][0-9]{6,7}-[0-9Kk]$"}
            ),
            # para que se pueda seleccionar fecha y hora
            'horaentrada': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            # para que se pueda seleccionar fecha y hora
            'horasalida': forms.DateTimeInput(
                attrs={'class': 'form-control','type': 'datetime-local'}
            ),
        }