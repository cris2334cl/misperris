from django.db import models
from django.contrib.auth.models import User

class Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    run_cliente = models.CharField(max_length=10)
    nombre_cliente = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.TextField()
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.run_cliente} - {self.nombre_cliente} {self.apellido}"

class Solicitud(models.Model):
    id = models.IntegerField(primary_key=True)
    run_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.PROTECT)
    detalle = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud {self.id} de {self.run_cliente.nombre_cliente}"


class SolicitudContacto(models.Model):
    TIPO_CHOICES = [
        ('adopcion', 'Adopción'),
        ('voluntariado', 'Voluntariado'),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mascota_interes = models.CharField(max_length=80, blank=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'solicitud de contacto'
        verbose_name_plural = 'solicitudes de contacto'

    def __str__(self):
        return f'{self.get_tipo_display()} de {self.nombre}'