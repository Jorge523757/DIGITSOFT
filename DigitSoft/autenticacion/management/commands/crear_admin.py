"""
Comando para crear un usuario administrador predeterminado
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from autenticacion.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Crea un usuario administrador predeterminado para DigitSoft'

    def handle(self, *args, **options):
        # Credenciales del administrador predeterminado
        username = 'admin'
        email = 'admin@digitsoft.com'
        password = 'Admin123456'

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe.')
            )
            return

        try:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Administrador',
                last_name='Sistema',
                is_staff=True,
                is_superuser=True
            )

            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                user=user,
                tipo_usuario='SUPER_ADMIN',
                documento='000000000',
                telefono='3000000000',
                estado='ACTIVO',
                puede_crear_usuarios=True
            )

            self.stdout.write(
                self.style.SUCCESS('✅ Usuario administrador creado exitosamente!')
            )
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('📋 Credenciales de acceso:'))
            self.stdout.write(self.style.SUCCESS(f'   Usuario: {username}'))
            self.stdout.write(self.style.SUCCESS(f'   Contraseña: {password}'))
            self.stdout.write(self.style.SUCCESS(f'   Tipo: Super Administrador'))
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING('⚠️  IMPORTANTE: Cambia la contraseña después del primer inicio de sesión')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al crear el usuario: {str(e)}')
            )

