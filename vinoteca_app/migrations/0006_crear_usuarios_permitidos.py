from django.db import migrations

def cargar_usuarios_permitidos_iniciales(apps, schema_editor):
    UsuarioPermitido = apps.get_model('vinoteca_app', 'UsuarioPermitido')

    usuarios_iniciales = [
        {
            'nombre': 'Analia',
            'email': 'annavillegas@live.com.ar',
            'codigo_validation': 'Ana2026/'
        },
        {
            'nombre': 'Sol',
            'email': 'skalapuj@gmail.com',
            'codigo_validation': 'Sol2026/'
        },
    ]

    for datos in usuarios_iniciales:
        UsuarioPermitido.objects.get_or_create(
            email=datos['email'],
            defaults={
                'nombre': datos['nombre'],
                'codigo_validation': datos['codigo_validation']
            }
        )

def eliminar_usuarios_permitidos_iniciales(apps, schema_editor):
    UsuarioPermitido = apps.get_model('vinoteca_app', 'UsuarioPermitido')
    UsuarioPermitido.objects.filter(email__in=[
        'annavillegas@live.com.ar',
        'skalapuj@gmail.com'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('vinoteca_app', '0005_contenidonosotros'),
    ]

    operations = [
        migrations.RunPython(
            cargar_usuarios_permitidos_iniciales, 
            eliminar_usuarios_permitidos_iniciales
        ),
    ]