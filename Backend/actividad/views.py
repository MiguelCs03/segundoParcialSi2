from django.shortcuts import render
from rest_framework import viewsets
from .models import Dimension, Actividad
from .serializers import DimensionSerializer, ActividadSerializer

class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
