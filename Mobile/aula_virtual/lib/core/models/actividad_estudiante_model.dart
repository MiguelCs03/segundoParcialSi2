class ActividadEstudianteModel {
  final int id;
  final String nombre;
  final String descripcion;
  final String estado;
  final String fechaCreacion;
  final String? fechaVencimiento;
  final double? nota;
  final String? comentario;

  ActividadEstudianteModel({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.estado,
    required this.fechaCreacion,
    this.fechaVencimiento,
    this.nota,
    this.comentario,
  });

  factory ActividadEstudianteModel.fromJson(Map<String, dynamic> json) {
    return ActividadEstudianteModel(
      id: json['id'] ?? 0,
      nombre: json['nombre'] ?? '',
      descripcion: json['descripcion'] ?? '',
      estado: json['estado'] ?? '',
      fechaCreacion: json['fecha_creacion'] ?? '',
      fechaVencimiento: json['fecha_vencimiento'],
      nota: json['nota']?.toDouble(),
      comentario: json['comentario'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'descripcion': descripcion,
      'estado': estado,
      'fecha_creacion': fechaCreacion,
      'fecha_vencimiento': fechaVencimiento,
      'nota': nota,
      'comentario': comentario,
    };
  }

  // 🔥 GETTERS ÚTILES
  bool get estaPendiente => estado.toLowerCase() == 'pendiente';
  bool get estaEntregada => estado.toLowerCase() == 'entregada';
  bool get estaRevisada => estado.toLowerCase() == 'revisada';

  @override
  String toString() {
    return 'ActividadEstudianteModel(id: $id, nombre: $nombre, estado: $estado)';
  }
}
