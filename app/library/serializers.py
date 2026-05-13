from django.utils import timezone
from rest_framework import serializers

from .models import Autor, Libro, Prestamo, Usuario


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = [
            "id",
            "nombre",
            "apellido",
            "fecha_registro",
        ]
        read_only_fields = [
            "id",
            "fecha_registro",
        ]


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "nombre",
            "apellido",
            "correo",
            "telefono",
            "activo",
            "fecha_registro",
        ]
        read_only_fields = [
            "id",
            "fecha_registro",
        ]


class LibroSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source="autor", read_only=True)

    class Meta:
        model = Libro
        fields = [
            "id",
            "titulo",
            "autor",
            "autor_nombre",
            "anio_publicacion",
            "ejemplares_disponibles",
            "activo",
            "fecha_registro",
        ]
        read_only_fields = [
            "id",
            "fecha_registro",
        ]

    def validate_anio_publicacion(self, value):
        if value and value > timezone.now().year:
            raise serializers.ValidationError(
                "El año de publicación no puede ser mayor al año actual."
            )

        return value


class PrestamoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source="usuario", read_only=True)
    libro_titulo = serializers.CharField(source="libro", read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            "id",
            "usuario",
            "usuario_nombre",
            "libro",
            "libro_titulo",
            "fecha_prestamo",
            "fecha_devolucion",
            "estado",
            "fecha_registro",
        ]
        read_only_fields = [
            "id",
            "fecha_registro",
        ]

    def validate(self, data):
        fecha_prestamo = data.get(
            "fecha_prestamo", getattr(self.instance, "fecha_prestamo", None)
        )
        fecha_devolucion = data.get(
            "fecha_devolucion", getattr(self.instance, "fecha_devolucion", None)
        )
        usuario = data.get("usuario", getattr(self.instance, "usuario", None))
        libro = data.get("libro", getattr(self.instance, "libro", None))
        estado = data.get("estado", getattr(self.instance, "estado", Prestamo.ACTIVO))

        if fecha_prestamo and fecha_devolucion:
            if fecha_devolucion < fecha_prestamo:
                raise serializers.ValidationError(
                    "La fecha de devolución no puede ser anterior a la fecha del préstamo."
                )

        if usuario and not usuario.activo:
            raise serializers.ValidationError(
                "No se puede registrar un préstamo para un usuario inactivo."
            )

        if libro and not libro.activo:
            raise serializers.ValidationError("No se puede prestar un libro inactivo.")

        if libro and estado == Prestamo.ACTIVO and libro.ejemplares_disponibles <= 0:
            raise serializers.ValidationError(
                "No hay ejemplares disponibles para este libro."
            )

        return data
