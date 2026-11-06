from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import MascotaForm, SolicitudContactoForm
from .models import Mascota


def home(request):
    adoption_form = SolicitudContactoForm(
        request.POST if request.method == 'POST' and 'adopcion-tipo' in request.POST else None,
        initial={'tipo': 'adopcion'},
        prefix='adopcion',
    )
    volunteer_form = SolicitudContactoForm(
        request.POST if request.method == 'POST' and 'voluntariado-tipo' in request.POST else None,
        initial={'tipo': 'voluntariado'},
        prefix='voluntariado',
    )

    if request.method == 'POST':
        form = volunteer_form if 'voluntariado-tipo' in request.POST else adoption_form
        if form.is_valid():
            form.save()
            messages.success(
                request,
                '¡Gracias! Recibimos tu solicitud y pronto nos pondremos en contacto contigo.',
            )
            return redirect('home')

    perritos = [
        {
            'nombre': 'Luna',
            'edad': '2 años',
            'tamano': 'Mediana',
            'descripcion': 'Cariñosa, tranquila y fanática de los paseos.',
            'imagen': 'https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=900&q=85',
        },
        {
            'nombre': 'Max',
            'edad': '1 año',
            'tamano': 'Mediano',
            'descripcion': 'Juguetón y sociable; siempre está listo para una aventura.',
            'imagen': 'https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=900&q=85',
        },
        {
            'nombre': 'Mora',
            'edad': '3 años',
            'tamano': 'Pequeña',
            'descripcion': 'Una compañera dulce que disfruta de los días en familia.',
            'imagen': 'https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?auto=format&fit=crop&w=900&q=85',
        },
    ]

    return render(
        request,
        'index.html',
        {
            'adoption_form': adoption_form,
            'volunteer_form': volunteer_form,
            'perritos': perritos,
        },
    )


def mascotas(request):
    mascotas_db = Mascota.objects.all().order_by('nombre')
    return render(request, 'mascotas.html', {'mascotas': mascotas_db})


@login_required(login_url='login')
def mascota_crear(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.usuario = request.user
            mascota.save()
            messages.success(request, 'La mascota fue creada correctamente.')
            return redirect('mascotas')
    else:
        form = MascotaForm()

    return render(request, 'mascota_form.html', {
        'form': form,
        'titulo': 'Crear mascota',
        'accion': 'Guardar',
    })


@login_required(login_url='login')
def mascota_editar(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de la mascota fueron actualizados.')
            return redirect('mascotas')
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'mascota_form.html', {
        'form': form,
        'titulo': 'Editar mascota',
        'accion': 'Actualizar',
        'mascota': mascota,
    })


@login_required(login_url='login')
def mascota_eliminar(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        if mascota.solicitud_set.exists():
            messages.error(
                request,
                'No se puede eliminar esta mascota porque tiene solicitudes asociadas.',
            )
            return redirect('mascotas')

        mascota.delete()
        messages.success(request, f'La mascota {mascota.nombre} fue eliminada.')
        return redirect('mascotas')

    return render(request, 'mascota_confirm_delete.html', {'mascota': mascota})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('mascotas')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('mascotas')

        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'Se cerró la sesión correctamente.')
    return redirect('home')
