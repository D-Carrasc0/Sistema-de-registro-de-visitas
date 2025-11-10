from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"registros", views.RegistroViewSet)

# Estas son las urls(rutas) del sitio web
urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # esta es la raiz la cual muestra la lista de registros
    path('registros/', views.lista_registros, name='lista_registros'),
    # esta es para agregar un nuevo registro
    path('registros/nuevo/', views.nuevo_registro, name='nuevo_registro'),
    # esta para ver el detalle de un registro
    path('registros/<int:pk>/', views.detalle_registro, name='detalle_registro'),
    # esta para editar un registro
    path('registros/<int:pk>/editar/', views.editar_registro, name='editar_registro'),
    # finalmente esta para eliminar un registro
    path('registros/<int:pk>/eliminar/', views.eliminar_registro, name='eliminar_registro'),
]