from django.contrib.auth.models import Group, User

# Importa la base de serializadores de rest_framework
from rest_framework import serializers
# Se importa el modelo de Registro
from .models import Registro

# Serializador para el modelo Registro
class RegistroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Registro
        fields = ['url', 'nombre', 'rut', 'motivo', 'horaentrada', 'horasalida', 'estado_finalizado']

# Serializador para el modelo User
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]

# Serializador para el modelo Group
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]