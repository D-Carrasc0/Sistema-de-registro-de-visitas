from django.urls import path, include
from . import views

# Importa el enrutador por defecto de rest_framework
from rest_framework import routers
# Importa las vistas para obtener y renovar tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Crea un router por defecto que generará automáticamente las rutas para los viewSets
router = routers.DefaultRouter()
# Se registra el viewSet de users bajo la ruta /api/users/
router.register(r"users", views.UserViewSet)
# Se registra el viewSet de groups bajo la ruta /api/groups/
router.register(r"groups", views.GroupViewSet)
# Se registra el ViewSet de usuarios bajo la ruta /api/registros/
router.register(r"registros", views.RegistroViewSet)

# Estas son las urls(rutas) del sitio web
urlpatterns = [
    # Rutas JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas API Rest
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/dashboard/", views.dashboard_stats, name="dashboard-stats"),


    # esta es la raiz la cual muestra la lista de registros
    path('', views.lista_registros, name='lista_registros'),
    # esta es para agregar un nuevo registro
    path('registros/nuevo/', views.nuevo_registro, name='nuevo_registro'),
    # esta para ver el detalle de un registro
    path('registros/<int:pk>/', views.detalle_registro, name='detalle_registro'),
    # esta para editar un registro
    path('registros/<int:pk>/editar/', views.editar_registro, name='editar_registro'),
    # finalmente esta para eliminar un registro
    path('registros/<int:pk>/eliminar/', views.eliminar_registro, name='eliminar_registro'),
]