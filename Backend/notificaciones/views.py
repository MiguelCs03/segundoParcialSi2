from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DispositivoToken
from .serializers import DispositivoTokenSerializer
from .firebase import enviar_notificacion, enviar_notificacion_multiple

class DispositivoTokenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DispositivoTokenSerializer
    
    def get_queryset(self):
        # Solo devuelve los tokens del usuario autenticado
        return DispositivoToken.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_token(request):
    """Registrar un token de dispositivo para el usuario"""
    token = request.data.get('token')
    
    if not token:
        return Response({"error": "Se requiere un token"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Crear o actualizar el token
    obj, created = DispositivoToken.objects.update_or_create(
        usuario=request.user,
        token=token,
        defaults={'activo': True}
    )
    
    return Response({
        "success": True,
        "created": created
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviar_prueba(request):
    """Enviar notificación de prueba al usuario"""
    tokens = DispositivoToken.objects.filter(
        usuario=request.user,
        activo=True
    ).values_list('token', flat=True)
    
    if not tokens:
        return Response({"error": "No hay dispositivos registrados"}, status=status.HTTP_404_NOT_FOUND)
    
    resultado = enviar_notificacion_multiple(
        list(tokens),
        "Notificación de prueba",
        "¡Esta es una notificación de prueba enviada desde el servidor!"
    )
    
    return Response(resultado)
# Create your views here.
