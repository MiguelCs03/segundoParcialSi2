from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, login_view, logout_view, cambiar_contrasena

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cambiar-contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
]

urlpatterns += router.urls