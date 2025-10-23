from django.db import models

# Create your models here.
# Se crea el modelo Registro
class Registro(models.Model):
    # Posee los siguientes campos
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=10, unique=True)
    motivo = models.TextField()
    horaentrada = models.DateTimeField()
    horasalida = models.DateTimeField(null=True, blank=True)
    # estado = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.nombre} - {self.rut}"