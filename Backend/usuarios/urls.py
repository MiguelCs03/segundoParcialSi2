from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UsuarioViewSet, LoginView, LogoutView, CambiarContrasenaView,
    CustomTokenObtainPairView, EstudiantesDelTutorView, ResumenAlumnoView,
    ResumenHijoTutorView, RendimientoDetalladoHijoView  # 👈 Nuevas vistas
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    # 👈 URLs originales en el mismo orden
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cambiar-contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    path('tutor/estudiantes/', EstudiantesDelTutorView.as_view(), name='estudiantes-tutor'),
    path('alumno/resumen/', ResumenAlumnoView.as_view(), name='alumno_resumen'),
    # 👈 Nuevas URLs para el dashboard del tutor
    path('tutor/hijo/<int:estudiante_id>/resumen/', ResumenHijoTutorView.as_view(), name='resumen_hijo_tutor'),
    path('tutor/hijo/<int:estudiante_id>/rendimiento/', RendimientoDetalladoHijoView.as_view(), name='rendimiento_hijo_tutor'),
]

urlpatterns += router.urls

urlpatterns += [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
