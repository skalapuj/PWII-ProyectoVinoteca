from django.apps import AppConfig

class VinotecaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vinoteca_app'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError

        def crear_superusuario(sender, **kwargs):
            # Al finalizar las migraciones de esta app
            if sender.name == 'vinoteca_app':
                try:
                    User = get_user_model()
                    if not User.objects.filter(username="postgres").exists():
                        User.objects.create_superuser(username="postgres", email="", password="Django")
                        print("Superusuario creado correctamente")
                    else:
                        print("El superusuario ya existe")
                except OperationalError:
                    print("La base de datos aún no está lista. Intentá de nuevo tras migraciones.")

        # Conexion a la función a la señal post_migrate
        post_migrate.connect(crear_superusuario, sender=self)