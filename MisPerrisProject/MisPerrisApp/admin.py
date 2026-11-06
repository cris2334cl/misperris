from django.contrib import admin
from .models import Cliente, Mascota, Solicitud, SolicitudContacto


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('run_cliente', 'nombre_cliente', 'apellido', 'correo', 'telefono')
    search_fields = ('run_cliente', 'nombre_cliente', 'apellido')

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'run_cliente', 'id_mascota', 'fecha')
    search_fields = ('run_cliente__nombre_cliente', 'id_mascota__nombre')
    list_filter = ('fecha',)


@admin.register(SolicitudContacto)
class SolicitudContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'tipo', 'mascota_interes', 'fecha')
    search_fields = ('nombre', 'email', 'mascota_interes')
    list_filter = ('tipo', 'fecha')
