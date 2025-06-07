import 'package:flutter/material.dart';
import '../services/profesor_service.dart';

class ProfesorProvider with ChangeNotifier {
  List<MateriaModel> _materias = [];
  List<EstudianteModel> _estudiantes = [];
  List<ActividadModel> _actividades = [];
  DestinatariosModel? _destinatarios;
  
  bool _isLoading = false;
  String? _errorMessage;

  // Getters
  List<MateriaModel> get materias => _materias;
  List<EstudianteModel> get estudiantes => _estudiantes;
  List<ActividadModel> get actividades => _actividades;
  DestinatariosModel? get destinatarios => _destinatarios;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  // 🔥 CARGAR MATERIAS
  Future<void> cargarMaterias() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _materias = await ProfesorService.obtenerMaterias();
      print('✅ Materias cargadas: ${_materias.length}');
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = 'Error al cargar materias: $e';
      _isLoading = false;
      notifyListeners();
      print('❌ Error cargando materias: $e');
    }
  }

  // 🔥 CARGAR ESTUDIANTES
  Future<void> cargarEstudiantes(int detalleId) async {
    _isLoading = true;
    notifyListeners();

    try {
      _estudiantes = await ProfesorService.obtenerEstudiantes(detalleId);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = 'Error al cargar estudiantes: $e';
      _isLoading = false;
      notifyListeners();
    }
  }

  // 🔥 CARGAR ACTIVIDADES
  Future<void> cargarActividades(int detalleId) async {
    try {
      _actividades = await ProfesorService.obtenerActividades(detalleId);
      notifyListeners();
    } catch (e) {
      _errorMessage = 'Error al cargar actividades: $e';
      notifyListeners();
    }
  }

  // 🔥 CARGAR DESTINATARIOS (CORREGIDO)
  Future<void> cargarDestinatarios({int? detalleMateriaId}) async {
    print('🚀 Iniciando cargarDestinatarios con materia: $detalleMateriaId');
    
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _destinatarios = await ProfesorService.obtenerDestinatarios(
        detalleMateriaId: detalleMateriaId
      );
      
      print('✅ Destinatarios cargados exitosamente');
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      print('❌ Error en cargarDestinatarios: $e');
      _errorMessage = 'Error al cargar destinatarios: $e';
      _isLoading = false;
      notifyListeners();
    }
  }

  // 🔥 ENVIAR NOTIFICACIÓN
  Future<Map<String, dynamic>?> enviarNotificacionMasiva({
    required List<int> destinatarios,
    required String titulo,
    required String mensaje,
    String tipo = 'general',
  }) async {
    try {
      final resultado = await ProfesorService.enviarNotificacionMasiva(
        destinatarios: destinatarios,
        titulo: titulo,
        mensaje: mensaje,
        tipo: tipo,
      );
      return resultado;
    } catch (e) {
      _errorMessage = 'Error al enviar notificación: $e';
      notifyListeners();
      return null;
    }
  }

  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }
}