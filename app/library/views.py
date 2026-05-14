from rest_framework import viewsets

from .models import Autor, Libro, Prestamo, Usuario
from .serializers import (
    AutorSerializer,
    LibroSerializer,
    PrestamoSerializer,
    UsuarioSerializer,
)


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.select_related("autor").all()
    serializer_class = LibroSerializer


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.select_related(
        "usuario",
        "libro",
    ).all()
    serializer_class = PrestamoSerializer
