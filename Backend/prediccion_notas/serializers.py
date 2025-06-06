from rest_framework import serializers
from .models import PrediccionNota

class PrediccionNotaSerializer(serializers.ModelSerializer):
    nombre_estudiante = serializers.SerializerMethodField()
    materia = serializers.SerializerMethodField()
    
    class Meta:
        model = PrediccionNota
        fields = ['id', 'estudiante', 'nombre_estudiante', 'detalle_materia', 
                  'materia', 'ser', 'saber', 'hacer', 'decidir', 
                  'nota_predicha', 'estado_predicho', 'fecha_prediccion']
        read_only_fields = ['id', 'nota_predicha', 'estado_predicho', 'fecha_prediccion']
    
    def get_nombre_estudiante(self, obj):
        return obj.estudiante.nombre if obj.estudiante else None
    
    def get_materia(self, obj):
        return obj.detalle_materia.materia.nombre if obj.detalle_materia else None