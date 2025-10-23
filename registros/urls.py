from django.urls import path
from . import views

# Estas son las urls(rutas) del sitio web
urlpatterns = [
    # esta es la raiz la cual muestra la lista de registros
    path('', views.lista_registros, name='lista_registros'),
    # esta es para agregar un nuevo registro
    path('registro/', views.nuevo_registro, name='nuevo_registro'),
    # esta para ver el detalle de un registro
    path('registros/<int:pk>/', views.detalle_registro, name='detalle_registro'),
    # esta para editar un registro
    path('registros/<int:pk>/editar/', views.editar_registro, name='editar_registro'),
    # finalmente esta para eliminar un registro
    path('registros/<int:pk>/eliminar/', views.eliminar_registro, name='eliminar_registro'),
]