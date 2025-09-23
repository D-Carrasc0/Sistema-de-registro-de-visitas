from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['nombre', 'rut', 'motivo', 'horaentrada', 'horasalida']
        widgets = {
            'horaentrada': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'horasalida': forms.DateTimeInput(
                attrs={'class': 'form-control','type': 'datetime-local'}
            ),
        }