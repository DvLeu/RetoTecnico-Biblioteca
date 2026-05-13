from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Autor, Libro, Prestamo, Usuario

# Register your models here.
@admin.register(Autor)
class AutorAdmin(ImportExportModelAdmin):
    list_display = (
        'nombre',
        'apellido',
        'fecha_registro',
    )
    search_fields = (
        'nombre',
        'apellido',
    )
    list_filter = (
        'fecha_registro',
    )


@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    list_display = (
        'nombre',
        'apellido',
        'correo',
        'telefono',
        'activo',
        'fecha_registro',
    )
    search_fields = (
        'nombre',
        'apellido',
        'correo',
    )
    list_filter = (
        'activo',
        'fecha_registro',
    )


@admin.register(Libro)
class LibroAdmin(ImportExportModelAdmin):
    list_display = (
        'titulo',
        'autor',
        'anio_publicacion',
        'ejemplares_disponibles',
        'activo',
        'fecha_registro',
    )
    search_fields = (
        'titulo',
        'autor__nombre',
        'autor__apellido',
    )
    list_filter = (
        'activo',
        'anio_publicacion',
        'fecha_registro',
    )


@admin.register(Prestamo)
class PrestamoAdmin(ImportExportModelAdmin):
    list_display = (
        'usuario',
        'libro',
        'fecha_prestamo',
        'fecha_devolucion',
        'estado',
        'fecha_registro',
    )
    search_fields = (
        'usuario__nombre',
        'usuario__apellido',
        'usuario__correo',
        'libro__titulo',
    )
    list_filter = (
        'estado',
        'fecha_prestamo',
        'fecha_devolucion',
        'fecha_registro',
    )