from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    NivelViewSet, MateriaViewSet, 
    DetalleMateriaViewSet, AsistenciaViewSet,
    MateriasDelProfesorView, MateriasDelAlumnoView,
    EstudiantesDeMateriaView,
    RegistrarAsistenciaDesdeLibreta,
    ObtenerAsistenciaPorFechaView,
    ReporteAsistenciaGestionView,
    MateriaDetalleAlumnoView
)

router = DefaultRouter()
router.register(r'niveles', NivelViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'detalles-materia', DetalleMateriaViewSet)
router.register(r'asistencias', AsistenciaViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('profesor/materias/', MateriasDelProfesorView.as_view(), name='materias-profesor'),
    path('alumno/materias/', MateriasDelAlumnoView.as_view(), name='materias-alumno'),
    path('profesor/materia/<int:detalle_id>/estudiantes/', EstudiantesDeMateriaView.as_view(), name='profesor-materia-estudiantes'),
    path('profesor/materia/<int:detalle_id>/registrar-asistencia/', RegistrarAsistenciaDesdeLibreta.as_view()),
    path('profesor/materia/<int:detalle_id>/asistencia-por-fecha/', ObtenerAsistenciaPorFechaView.as_view()),
    path('profesor/materia/<int:detalle_id>/reporte-asistencia/', ReporteAsistenciaGestionView.as_view()),
    path('alumno/materia/<int:detalle_id>/detalle/', MateriaDetalleAlumnoView.as_view(), name='detalle-materia-alumno'),
]

