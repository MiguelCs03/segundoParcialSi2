from django.shortcuts import render
from Backend.permissions import SoloUsuariosConRol
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Nivel, Materia, DetalleMateria, Asistencia
)
from .serializers import (
    NivelSerializer, MateriaSerializer, 
     DetalleMateriaSerializer, AsistenciaSerializer
)

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    #permission_classes = [SoloUsuariosConRol]

class DetalleMateriaViewSet(viewsets.ModelViewSet):
    queryset = DetalleMateria.objects.all()
    serializer_class = DetalleMateriaSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class MateriasDelProfesorView(APIView):
    #permission_classes = [IsAuthenticated]  # puedes dejarla comentada si estás probando sin login

    def get(self, request):
        profesor = request.user
        detalles = DetalleMateria.objects.filter(profesor=profesor).select_related('materia', 'curso__paralelo')

        resultado = []
        for d in detalles:
            resultado.append({
                'materia': d.materia.nombre,
                'nivel': d.materia.nivel.get_nombre_display(),
                'curso': d.curso.nombre,
                'paralelo': d.curso.paralelo.nombre
            })

        return Response(resultado)