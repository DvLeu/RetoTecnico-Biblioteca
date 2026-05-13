import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Autor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre', 'apellido']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'.strip()


class Usuario(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre', 'apellido']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Libro(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(
        Autor,
        on_delete=models.PROTECT,
        related_name='libros'
    )
    anio_publicacion = models.PositiveIntegerField(blank=True, null=True)
    ejemplares_disponibles = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def clean(self):
        anio_actual = timezone.now().year

        if self.anio_publicacion and self.anio_publicacion > anio_actual:
            raise ValidationError(
                'El año de publicación no puede ser mayor al año actual.'
            )

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    ACTIVO = 'activo'
    DEVUELTO = 'devuelto'
    VENCIDO = 'vencido'

    ESTADOS = [
        (ACTIVO, 'Activo'),
        (DEVUELTO, 'Devuelto'),
        (VENCIDO, 'Vencido'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='prestamos'
    )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,
        related_name='prestamos'
    )
    fecha_prestamo = models.DateField(default=timezone.localdate)
    fecha_devolucion = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ACTIVO
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def clean(self):
        if self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError(
                'La fecha de devolución no puede ser anterior a la fecha del préstamo.'
            )

        if self.usuario_id and not self.usuario.activo:
            raise ValidationError(
                'No se puede registrar un préstamo para un usuario inactivo.'
            )

        if self.libro_id and not self.libro.activo:
            raise ValidationError(
                'No se puede prestar un libro inactivo.'
            )

        if (
            self.libro_id
            and self.estado == self.ACTIVO
            and self.libro.ejemplares_disponibles <= 0
        ):
            raise ValidationError(
                'No hay ejemplares disponibles para este libro.'
            )

    def __str__(self):
        return f'{self.usuario} - {self.libro}'