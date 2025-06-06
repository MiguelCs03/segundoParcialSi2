from django.db import models
from usuarios.models import Usuario
from materia.models import DetalleMateria
from libreta.models import Libreta

class PrediccionNota(models.Model):
    # Relación con Estudiante y Libreta
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='predicciones')
    libreta = models.ForeignKey(Libreta, on_delete=models.CASCADE, related_name='predicciones', null=True)
    detalle_materia = models.ForeignKey(DetalleMateria, on_delete=models.CASCADE, related_name='predicciones')
    
    # Dimensiones de evaluación
    ser = models.FloatField(null=True, blank=True)
    saber = models.FloatField(null=True, blank=True)
    hacer = models.FloatField(null=True, blank=True)
    decidir = models.FloatField(null=True, blank=True)
    
    # Resultados de predicción
    nota_predicha = models.DecimalField(max_digits=5, decimal_places=2)
    estado_predicho = models.CharField(max_length=20)  # 'Aprobado' o 'Reprobado'
    
    # Metadatos
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Predicción de Nota"
        verbose_name_plural = "Predicciones de Notas"
    
    def __str__(self):
        return f"Predicción {self.estudiante.nombre} - {self.detalle_materia.materia.nombre}: {self.nota_predicha}"
