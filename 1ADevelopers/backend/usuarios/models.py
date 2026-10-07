from django.db import models

class Rol(models.Model):
    # id_rol se crea automáticamente como un campo autoincremental
    nombre_rol = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"