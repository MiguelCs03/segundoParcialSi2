from rest_framework.routers import DefaultRouter
from .views import (
    NivelViewSet, MateriaViewSet, 
    DetalleMateriaViewSet, AsistenciaViewSet
)

router = DefaultRouter()
router.register(r'niveles', NivelViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'detalles-materia', DetalleMateriaViewSet)
router.register(r'asistencias', AsistenciaViewSet)

urlpatterns = router.urls