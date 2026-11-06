from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Crea o actualiza el usuario administrador de demostracion desde .env.'

    def handle(self, *args, **options):
        username = getattr(settings, 'DEMO_USERNAME', '')
        password = getattr(settings, 'DEMO_PASSWORD', '')

        if not username or not password:
            raise CommandError(
                'Configura DEMO_USERNAME y DEMO_PASSWORD en el archivo .env.'
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username=username)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = 'creado' if created else 'actualizado'
        self.stdout.write(self.style.SUCCESS(
            f'Usuario de demostracion "{username}" {action} correctamente.'
        ))
