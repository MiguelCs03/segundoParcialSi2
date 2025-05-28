from rest_framework.routers import DefaultRouter
from .views import DimensionViewSet, ActividadViewSet  # Elimina DetalleActividadViewSet

router = DefaultRouter()
router.register(r'dimensiones', DimensionViewSet)
router.register(r'actividades', ActividadViewSet)

urlpatterns = router.urls