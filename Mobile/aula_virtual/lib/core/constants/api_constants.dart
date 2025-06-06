class ApiConstants {
  // 🔄 Cambiar por tu IP de Wi-Fi
  static const String baseUrl = 'http://192.168.0.5:8000';
  static const String apiUrl = '$baseUrl/api';
  
  // Auth endpoints
  static const String loginEndpoint = '$apiUrl/login/';
  static const String tokenRefreshEndpoint = '$apiUrl/token/refresh/';
  
  // Profesor endpoints
  static const String profesorMateriasEndpoint = '$apiUrl/profesor/materias/';
  
  // Estudiante endpoints
  static const String estudianteResumenEndpoint = '$apiUrl/alumno/resumen/';
  
  // Tutor endpoints
  static const String tutorEstudiantesEndpoint = '$apiUrl/tutor/estudiantes/';
}