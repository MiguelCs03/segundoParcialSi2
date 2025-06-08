import 'actividad_estudiante_model.dart';

class ResumenDashboardModel {
  final double promedioGeneral;
  final double asistenciaGeneral;
  final int materiasTotal;
  final int actividadesPendientes;
  final List<ActividadEstudianteModel> ultimasActividades;

  ResumenDashboardModel({
    required this.promedioGeneral,
    required this.asistenciaGeneral,
    required this.materiasTotal,
    required this.actividadesPendientes,
    required this.ultimasActividades,
  });

  factory ResumenDashboardModel.fromJson(Map<String, dynamic> json) {
  return ResumenDashboardModel(
    promedioGeneral: (json['promedio_general'] ?? 0).toDouble(),
    asistenciaGeneral: (json['asistencia_general'] ?? 0).toDouble(),
    materiasTotal: json['materias_total'] ?? 0,
    actividadesPendientes: json['actividades_pendientes'] ?? 0,
    ultimasActividades: (json['ultimas_actividades'] as List<dynamic>? ?? [])
        .map((item) => ActividadEstudianteModel.fromJson(item))
        .toList(),
  );
}

Map<String, dynamic> toJson() {
  return {
    'promedio_general': promedioGeneral,
    'asistencia_general': asistenciaGeneral,
    'materias_total': materiasTotal,
    'actividades_pendientes': actividadesPendientes,
    'ultimas_actividades': ultimasActividades.map((item) => item.toJson()).toList(),
  };
}


  @override
  String toString() {
    return 'ResumenDashboardModel(promedio: $promedioGeneral, asistencia: $asistenciaGeneral)';
  }
}