from django.db import models
from usuarios.models import Usuario
from materia.models import DetalleMateria

class Dimension(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='actividades')
    fecha = models.DateField(auto_now_add=True)  # Fecha de creación automática
    detalle_materia = models.ForeignKey(DetalleMateria, on_delete=models.CASCADE, related_name='actividades')
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Campo para la calificación

    def __str__(self):
        return f"{self.nombre} - Calificación: {self.calificacion}"
