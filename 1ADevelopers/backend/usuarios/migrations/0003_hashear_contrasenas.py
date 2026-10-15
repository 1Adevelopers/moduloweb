from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import migrations


def hashear_contrasenas(apps, schema_editor):
    """Convierte a hash las contraseñas que todavía estén guardadas en texto plano."""
    Usuario = apps.get_model('usuarios', 'Usuario')
    for usuario in Usuario.objects.all():
        try:
            identify_hasher(usuario.contrasena)
        except ValueError:
            usuario.contrasena = make_password(usuario.contrasena)
            usuario.save(update_fields=['contrasena'])


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_rol_id_alter_usuario_id'),
    ]

    operations = [
        migrations.RunPython(hashear_contrasenas, migrations.RunPython.noop),
    ]