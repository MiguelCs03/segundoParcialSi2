from django.shortcuts import render
from rest_framework import viewsets
from .models import Dimension, Actividad, DetalleActividad
from .serializers import DimensionSerializer, ActividadSerializer, DetalleActividadSerializer

class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

class DetalleActividadViewSet(viewsets.ModelViewSet):
    queryset = DetalleActividad.objects.all()
    serializer_class = DetalleActividadSerializer
