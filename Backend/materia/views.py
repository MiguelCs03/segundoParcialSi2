from django.shortcuts import render
from Backend.permissions import SoloUsuariosConRol
from rest_framework import viewsets
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
    permission_classes = [SoloUsuariosConRol]

class DetalleMateriaViewSet(viewsets.ModelViewSet):
    queryset = DetalleMateria.objects.all()
    serializer_class = DetalleMateriaSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer