from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_registros, name='lista_registros'),
    path('registro/', views.nuevo_registro, name='nuevo_registro'),
    path('registros/<int:pk>/', views.detalle_registro, name='detalle_registro'),
    path('registros/<int:pk>/editar/', views.editar_registro, name='editar_registro'),
    path('registros/<int:pk>/eliminar/', views.eliminar_registro, name='eliminar_registro'),
]