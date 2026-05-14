from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AutorViewSet,
    LibroViewSet,
    PrestamoViewSet,
    UsuarioViewSet,
    cerrar_sesion,
    prestamo_crear,
    prestamo_editar,
    prestamo_eliminar,
    prestamos_lista,
)


router = DefaultRouter()
router.register("autores", AutorViewSet)
router.register("usuarios", UsuarioViewSet)
router.register("libros", LibroViewSet)
router.register("prestamos", PrestamoViewSet)


urlpatterns = [
    path("api/", include(router.urls)),

    path("prestamos/", prestamos_lista, name="prestamos_lista"),
    path("prestamos/nuevo/", prestamo_crear, name="prestamo_crear"),
    path("prestamos/<uuid:pk>/editar/", prestamo_editar, name="prestamo_editar"),
    path("prestamos/<uuid:pk>/eliminar/", prestamo_eliminar, name="prestamo_eliminar"),
    
    path("logout/", cerrar_sesion, name="cerrar_sesion"),
]