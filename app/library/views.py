from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from django.contrib.auth import logout
from .forms import PrestamoForm
from .models import Autor, Libro, Prestamo, Usuario
from .serializers import AutorSerializer, LibroSerializer, PrestamoSerializer, UsuarioSerializer

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


@login_required
def prestamos_lista(request):
    prestamos = Prestamo.objects.select_related("usuario", "libro").all()

    return render(
        request,
        "library/prestamos_lista.html",
        {"prestamos": prestamos},
    )


@login_required
def prestamo_crear(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Préstamo registrado correctamente.")
            return redirect("prestamos_lista")
    else:
        form = PrestamoForm()

    return render(
        request,
        "library/prestamo_form.html",
        {
            "form": form,
            "titulo": "Nuevo préstamo",
        },
    )


@login_required
def prestamo_editar(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)

    if request.method == "POST":
        form = PrestamoForm(request.POST, instance=prestamo)

        if form.is_valid():
            form.save()
            messages.success(request, "Préstamo actualizado correctamente.")
            return redirect("prestamos_lista")
    else:
        form = PrestamoForm(instance=prestamo)

    return render(
        request,
        "library/prestamo_form.html",
        {
            "form": form,
            "titulo": "Editar préstamo",
        },
    )


@login_required
def prestamo_eliminar(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)

    if request.method == "POST":
        prestamo.delete()
        messages.success(request, "Préstamo eliminado correctamente.")
        return redirect("prestamos_lista")

    return render(
        request,
        "library/prestamo_confirmar_eliminar.html",
        {"prestamo": prestamo},
    )

@login_required
def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
        return redirect("admin:login")

    return redirect("prestamos_lista")