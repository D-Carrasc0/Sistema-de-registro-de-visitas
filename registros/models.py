from django.db import models

# Create your models here.
class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=10, unique=True)
    motivo = models.TextField()
    horaentrada = models.DateTimeField()
    horasalida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.rut}"