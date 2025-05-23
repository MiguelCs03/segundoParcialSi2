from django.db import models
from usuarios.models import Usuario
# Create your models here.

class Dimension(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='actividades')

    def __str__(self):
        return self.nombre

class DetalleActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='detalles_actividad')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='detalles_actividad')
    fecha = models.DateField(auto_now_add=True)  # Puedes agregar más campos si lo necesitas

    def __str__(self):
        return f"{self.usuario} - {self.actividad} ({self.fecha})"