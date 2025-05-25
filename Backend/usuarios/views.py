from rest_framework import viewsets, status
from .models import Usuario
from .serializers import UsuarioSerializer, CustomTokenObtainPairSerializer
from .serializers import UsuarioSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Login JWT usando el campo 'codigo'
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Puedes seguir usando este LoginView si quieres login manual:
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login con código y contraseña. Devuelve access y refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'codigo': openapi.Schema(type=openapi.TYPE_STRING, description='Código de usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña'),
            },
            required=['codigo', 'password'],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
        }
    )
    def post(self, request):
        codigo = request.data.get('codigo')
        password = request.data.get('password')
        user = authenticate(request, username=codigo, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'detail': 'Login exitoso',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'usuario': UsuarioSerializer(user).data,
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Código o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout del usuario autenticado (JWT).",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
        }
    )
    def post(self, request):
        # Para JWT, el "logout" es solo borrar el token en el cliente.
        # Si quieres invalidar el refresh token, puedes hacer un blacklist si tienes habilitado.
        return Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)

class CambiarContrasenaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Permite al usuario autenticado cambiar su contraseña.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña actual'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='Nueva contraseña'),
            },
            required=['old_password', 'new_password'],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
        }
    )
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'detail': 'Contraseña actual incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({'detail': 'Debes proporcionar una nueva contraseña.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'detail': '¡Contraseña actualizada correctamente!'}, status=status.HTTP_200_OK)
