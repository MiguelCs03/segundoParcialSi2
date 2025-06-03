from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dispositivos', views.DispositivoTokenViewSet, basename='dispositivo')

urlpatterns = [
    path('', include(router.urls)),
    path('registrar-token/', views.registrar_token, name='registrar-token'),
    path('enviar-prueba/', views.enviar_prueba, name='enviar-prueba'),
]