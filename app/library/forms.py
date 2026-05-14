from django import forms

from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            "usuario",
            "libro",
            "fecha_prestamo",
            "fecha_devolucion",
            "estado",
        ]
        widgets = {
            "fecha_prestamo": forms.DateInput(attrs={"type": "date"}),
            "fecha_devolucion": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        fecha_prestamo = cleaned_data.get("fecha_prestamo")
        fecha_devolucion = cleaned_data.get("fecha_devolucion")
        usuario = cleaned_data.get("usuario")
        libro = cleaned_data.get("libro")
        estado = cleaned_data.get("estado")

        if fecha_prestamo and fecha_devolucion and fecha_devolucion < fecha_prestamo:
            raise forms.ValidationError(
                "La fecha de devolución no puede ser anterior a la fecha del préstamo."
            )

        if usuario and not usuario.activo:
            raise forms.ValidationError(
                "No se puede registrar un préstamo para un usuario inactivo."
            )

        if libro and not libro.activo:
            raise forms.ValidationError(
                "No se puede prestar un libro inactivo."
            )

        if (
            libro
            and estado == Prestamo.ACTIVO
            and libro.ejemplares_disponibles <= 0
        ):
            raise forms.ValidationError(
                "No hay ejemplares disponibles para este libro."
            )

        return cleaned_data