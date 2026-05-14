from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AutorViewSet,
    LibroViewSet,
    PrestamoViewSet,
    UsuarioViewSet,
)


router = DefaultRouter()
router.register("autores", AutorViewSet)
router.register("usuarios", UsuarioViewSet)
router.register("libros", LibroViewSet)
router.register("prestamos", PrestamoViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
]