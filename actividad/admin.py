from django.contrib import admin
from .models import Dimension, Actividad, DetalleActividad
# Register your models here.
admin.site.register(Dimension)
admin.site.register(Actividad)
admin.site.register(DetalleActividad)