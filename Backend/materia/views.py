from django.shortcuts import render
from Backend.permissions import SoloUsuariosConRol
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from libreta.models import Libreta
from .models import (
    Nivel, Materia, DetalleMateria, Asistencia,
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
                'detalle_id': d.id, 
                'materia': d.materia.nombre,
                'nivel': d.materia.nivel.get_nombre_display(),
                'curso': d.curso.nombre,
                'paralelo': d.curso.paralelo.nombre
            })

        return Response(resultado)
    
class MateriasDelAlumnoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alumno = request.user

        libretas = Libreta.objects.filter(estudiante=alumno).select_related(
            'detalle_materia__materia',
            'detalle_materia__curso__paralelo',
            'detalle_materia__profesor'
        )
        
        materias_set = set()
        resultado = []
        for libreta in libretas:
            detalle = libreta.detalle_materia
            if detalle and detalle.id not in materias_set:
                materias_set.add(detalle.id)
                profesor = detalle.profesor
                resultado.append({
                    'materia': detalle.materia.nombre,
                    'nivel': detalle.materia.nivel.get_nombre_display(),
                    'curso': detalle.curso.nombre,
                    'paralelo': detalle.curso.paralelo.nombre,
                    'profesor': profesor.nombre if profesor else 'Profesor no asignado'
                })

        return Response(resultado)

class EstudiantesDeMateriaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, detalle_id):
        profesor = request.user

        try:
            detalle = DetalleMateria.objects.get(id=detalle_id, profesor=profesor)
        except DetalleMateria.DoesNotExist:
            return Response({'error': 'Materia no encontrada o no autorizada'}, status=403)

        libretas = Libreta.objects.filter(detalle_materia=detalle).select_related('estudiante')
        
        resultado = []
        for libreta in libretas:
            estudiante = libreta.estudiante
            resultado.append({
                'id': estudiante.id,
                'nombre': estudiante.nombre,
               # 'promedio': libreta.promedio if hasattr(libreta, 'promedio') else 'N/A'
            })

        return Response(resultado)