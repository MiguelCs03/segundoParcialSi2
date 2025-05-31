from django.shortcuts import render
from Backend.permissions import SoloUsuariosConRol
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date

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
                'libreta_id': libreta.id
               # 'promedio': libreta.promedio if hasattr(libreta, 'promedio') else 'N/A'
            })

        return Response(resultado)
    
class RegistrarAsistenciaDesdeLibreta(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, detalle_id):
        profesor = request.user
        print(f"[DEBUG] Profesor autenticado: {profesor}")

        try:
            detalle = DetalleMateria.objects.get(id=detalle_id, profesor=profesor)
            print(f"[DEBUG] DetalleMateria encontrado: {detalle}")
        except DetalleMateria.DoesNotExist:
            print(f"[ERROR] No autorizado para la materia id={detalle_id}")
            return Response({'error': 'No autorizado para esta materia'}, status=403)

        datos = request.data
        print(f"[DEBUG] Datos recibidos: {datos}")

        if not isinstance(datos, list):
            print("[ERROR] No es una lista de asistencias")
            return Response({'error': 'Se espera una lista de asistencias'}, status=400)

        resultados = []
        errores = []

        for item in datos:
            print(f"[DEBUG] Procesando item: {item}")
            libreta_id = item.get('libreta_id')
            presente = item.get('presente')

            try:
                libreta = Libreta.objects.get(id=libreta_id, detalle_materia=detalle)
                print(f"[DEBUG] Libreta encontrada: {libreta} - estudiante: {libreta.estudiante}")
            except Libreta.DoesNotExist:
                error_msg = f"Libreta {libreta_id} no pertenece a esta materia"
                print(f"[ERROR] {error_msg}")
                errores.append(error_msg)
                continue

            # Verificar duplicados para hoy
            if Asistencia.objects.filter(
                detalle_materia=detalle,
                estudiante=libreta.estudiante,
                fecha=date.today()
            ).exists():
                error_msg = f"Asistencia para libreta {libreta_id} ya existe hoy"
                print(f"[ERROR] {error_msg}")
                errores.append(error_msg)
                continue

            # Crear la asistencia
            asistencia = Asistencia.objects.create(
                detalle_materia=detalle,
                estudiante=libreta.estudiante,
                presente=presente
            )
            print(f"[DEBUG] Asistencia creada: {asistencia}")

            resultados.append({
                'estudiante': libreta.estudiante.nombre,
                'presente': presente
            })

        print(f"[DEBUG] Resultado final - creados: {resultados}, errores: {errores}")
        return Response({
            'mensaje': 'Proceso completado',
            'creados': resultados,
            'errores': errores
        }, status=status.HTTP_201_CREATED)
    
class ObtenerAsistenciaPorFechaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, detalle_id):
        profesor = request.user
        fecha_str = request.query_params.get('fecha', None)
        fecha = date.today()
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except Exception:
                pass

        try:
            detalle = DetalleMateria.objects.get(id=detalle_id, profesor=profesor)
        except DetalleMateria.DoesNotExist:
            return Response({'error': 'No autorizado para esta materia'}, status=403)

        asistencias = Asistencia.objects.filter(detalle_materia=detalle, fecha=fecha).select_related('estudiante')

        resultado = []
        for a in asistencias:
            resultado.append({
                'estudiante_id': a.estudiante.id,
                'nombre': a.estudiante.nombre,
                'presente': a.presente
            })

        return Response({'fecha': fecha, 'asistencias': resultado})
    
class ReporteAsistenciaGestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, detalle_id):
        profesor = request.user

        try:
            detalle = DetalleMateria.objects.get(id=detalle_id, profesor=profesor)
        except DetalleMateria.DoesNotExist:
            return Response({'error': 'No autorizado'}, status=403)

        # Obtener fechas únicas ordenadas
        fechas = list(
            Asistencia.objects.filter(detalle_materia=detalle)
            .order_by('fecha')
            .values_list('fecha', flat=True)
            .distinct()
        )

        # Obtener estudiantes (libretas) de la materia
        libretas = Libreta.objects.filter(detalle_materia=detalle).select_related('estudiante')

        resultado = []
        for libreta in libretas:
            fila = {'nombre': libreta.estudiante.nombre, 'asistencias': []}
            for fecha in fechas:
                asistencia = Asistencia.objects.filter(
                    detalle_materia=detalle,
                    estudiante=libreta.estudiante,
                    fecha=fecha
                ).first()
                fila['asistencias'].append(asistencia.presente if asistencia else False)
            resultado.append(fila)

        fechas_str = [f.isoformat() for f in fechas]

        return Response({'fechas': fechas_str, 'estudiantes': resultado})