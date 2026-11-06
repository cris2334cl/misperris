from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Mascota, Solicitud


class MascotaCrudAuthTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester',
            email='tester@example.com',
            password='12345678',
        )

    def test_public_list_is_accessible_without_login(self):
        response = self.client.get(reverse('mascotas'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_create_mascota(self):
        response = self.client.get(reverse('mascota_crear'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logged_user_can_create_mascota(self):
        self.client.login(username='tester', password='12345678')
        response = self.client.post(reverse('mascota_crear'), {'nombre': 'Coco'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Mascota.objects.filter(nombre='Coco', usuario=self.user).exists())

    def test_logged_user_can_edit_mascota(self):
        mascota = Mascota.objects.create(nombre='Coco', usuario=self.user)
        self.client.login(username='tester', password='12345678')

        response = self.client.post(
            reverse('mascota_editar', args=[mascota.pk]),
            {'nombre': 'Luna'},
        )

        self.assertRedirects(response, reverse('mascotas'))
        mascota.refresh_from_db()
        self.assertEqual(mascota.nombre, 'Luna')

    def test_logged_user_can_delete_mascota_without_solicitudes(self):
        mascota = Mascota.objects.create(nombre='Coco', usuario=self.user)
        self.client.login(username='tester', password='12345678')

        response = self.client.post(reverse('mascota_eliminar', args=[mascota.pk]))

        self.assertRedirects(response, reverse('mascotas'))
        self.assertFalse(Mascota.objects.filter(pk=mascota.pk).exists())

    def test_mascota_with_solicitud_cannot_be_deleted(self):
        mascota = Mascota.objects.create(nombre='Coco', usuario=self.user)
        cliente = Cliente.objects.create(
            run_cliente='12345678-9',
            nombre_cliente='Ana',
            apellido='Pérez',
            correo='ana@example.com',
            telefono='912345678',
        )
        Solicitud.objects.create(
            id=1,
            run_cliente=cliente,
            id_mascota=mascota,
            detalle='Solicitud de adopción',
        )
        self.client.login(username='tester', password='12345678')

        response = self.client.post(reverse('mascota_eliminar', args=[mascota.pk]))

        self.assertRedirects(response, reverse('mascotas'))
        self.assertTrue(Mascota.objects.filter(pk=mascota.pk).exists())
        self.assertTrue(Solicitud.objects.filter(id_mascota=mascota).exists())

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            f"{reverse('login')}?next=https://example.com",
            {'username': 'tester', 'password': '12345678'},
        )

        self.assertRedirects(response, reverse('mascotas'))

    def test_logout_ends_session(self):
        self.client.login(username='tester', password='12345678')

        response = self.client.get(reverse('logout'))

        self.assertRedirects(response, reverse('home'))
        response = self.client.get(reverse('mascota_crear'))
        self.assertEqual(response.status_code, 302)

    @override_settings(DEMO_USERNAME='demo', DEMO_PASSWORD='DemoPassword-2026!')
    def test_demo_user_command_creates_admin_user(self):
        call_command('crear_usuario_demo', stdout=None)

        demo_user = get_user_model().objects.get(username='demo')
        self.assertTrue(demo_user.is_staff)
        self.assertTrue(demo_user.is_superuser)
        self.assertTrue(demo_user.check_password('DemoPassword-2026!'))
