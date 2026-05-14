#!/bin/sh

set -e

echo "Esperando PostgreSQL..."

python << END
import os
import time
import psycopg2

host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", "5432")
db = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")

while True:
    try:
        psycopg2.connect(
            host=host,
            port=port,
            dbname=db,
            user=user,
            password=password,
        )
        break
    except psycopg2.OperationalError:
        time.sleep(1)

print("PostgreSQL disponible.")
END

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Creando usuario de prueba..."
python manage.py shell << END
from django.contrib.auth import get_user_model

User = get_user_model()

username = "appix"
email = "appix@appix.com"
password = "retoappix"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print("Superusuario creado.")
else:
    print("El superusuario ya existe.")
END

echo "Creando datos de prueba..."
python manage.py shell << END
from datetime import date, timedelta

from library.models import Autor, Usuario, Libro, Prestamo

autor, _ = Autor.objects.get_or_create(
    nombre="Gabriel",
    apellido="García Márquez",
)

usuario, _ = Usuario.objects.get_or_create(
    correo="juan@example.com",
    defaults={
        "nombre": "Juan",
        "apellido": "Pérez",
        "telefono": "2291234567",
        "activo": True,
    },
)

libro, _ = Libro.objects.get_or_create(
    titulo="Cien años de soledad",
    autor=autor,
    defaults={
        "anio_publicacion": 1967,
        "ejemplares_disponibles": 3,
        "activo": True,
    },
)

if not Prestamo.objects.filter(usuario=usuario, libro=libro).exists():
    Prestamo.objects.create(
        usuario=usuario,
        libro=libro,
        fecha_prestamo=date.today(),
        fecha_devolucion=date.today() + timedelta(days=7),
        estado=Prestamo.ACTIVO,
    )
    print("Préstamo de prueba creado.")
else:
    print("El préstamo de prueba ya existe.")
END

echo "Levantando servidor Django..."
exec "$@"