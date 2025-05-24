from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class LoginView(APIView):
    def post(self, request):
        codigo = request.data.get('codigo')
        password = request.data.get('password')
        user = authenticate(request, username=codigo, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Login exitoso'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Código o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)

class CambiarContrasenaView(APIView):
    permission_classes = [IsAuthenticated]

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
        update_session_auth_hash(request, user)
        return Response({'detail': '¡Contraseña actualizada correctamente!'}, status=status.HTTP_200_OK)