from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    NivelViewSet, MateriaViewSet, 
    DetalleMateriaViewSet, AsistenciaViewSet,
    MateriasDelProfesorView  # 👈 importar la vista personalizada
)

router = DefaultRouter()
router.register(r'niveles', NivelViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'detalles-materia', DetalleMateriaViewSet)
router.register(r'asistencias', AsistenciaViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('profesor/materias/', MateriasDelProfesorView.as_view(), name='materias-profesor'),
]

