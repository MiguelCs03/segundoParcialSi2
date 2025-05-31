from django.db import models
from usuarios.models import Usuario
from curso.models import Curso, Paralelo

class Nivel(models.Model):
    OPCIONES_NIVEL = (
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
    )
    nombre = models.CharField(max_length=20, choices=OPCIONES_NIVEL, unique=True)

    def __str__(self):
        return self.get_nombre_display()

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name='materias')

    def __str__(self):
        return f"{self.nombre} ({self.nivel})"

class DetalleMateria(models.Model):
    profesor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='detalles_materia',
        help_text="Profesor asignado a la materia"
    )
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='detalles_materia')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='detalles_materia', null=True, blank=True)

    def __str__(self):
        return f"{self.profesor} - {self.materia} - Curso: {self.curso}"

class Asistencia(models.Model):
    detalle_materia = models.ForeignKey(DetalleMateria, on_delete=models.CASCADE, related_name='asistencias')
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='asistencias', help_text="Alumno relacionado con la asistencia")  # Nuevo campo
    fecha = models.DateField(auto_now_add=True)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"Asistencia de {self.alumno} en {self.detalle_materia} ({self.fecha})"