from rest_framework.routers import DefaultRouter
from .views import (
   DimensionViewSet, ActividadViewSet,
    DetalleActividadViewSet, 
)

router = DefaultRouter()
router.register(r'dimensiones', DimensionViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'detalles-actividad', DetalleActividadViewSet)

urlpatterns = router.urls