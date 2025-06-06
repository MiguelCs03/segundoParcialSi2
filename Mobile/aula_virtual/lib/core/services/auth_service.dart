import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import '../constants/api_constants.dart';
import '../models/user_model.dart';
import '../utils/storage.util.dart';
import 'dart:async';

class AuthService extends ChangeNotifier {
  User? _currentUser;
  String? _accessToken;
  bool _isLoggedIn = false;

  User? get currentUser => _currentUser;
  String? get accessToken => _accessToken;
  bool get isLoggedIn => _isLoggedIn;
  String? get userRole => _currentUser?.rol;

  // Inicializar el servicio al abrir la app
  Future<void> init() async {
    await _loadStoredAuth();
  }

  Future<void> _loadStoredAuth() async {
    _accessToken = await StorageUtil.getAccessToken();
    final userData = await StorageUtil.getUserData();
    
    if (_accessToken != null && userData != null) {
      _currentUser = User.fromJson(userData);
      _isLoggedIn = true;
      notifyListeners();
    }
  }

  Future<LoginResult> login(String codigo, String password) async {
    try {
      final url = ApiConstants.loginEndpoint;
      print('🚀 Intentando conectar a: $url');
      print('📱 Datos: codigo=$codigo, password=${password.length} chars');
      
      final request = http.Request('POST', Uri.parse(url));
      request.headers['Content-Type'] = 'application/json';
      request.body = json.encode({
        'codigo': codigo,
        'password': password,
      });
      
      print('📤 Headers: ${request.headers}');
      print('📤 Body: ${request.body}');
      
      final streamedResponse = await request.send().timeout(
        Duration(seconds: 15),
        onTimeout: () {
          throw TimeoutException('Conexión timeout después de 15 segundos');
        },
      );
      
      final response = await http.Response.fromStream(streamedResponse);
      
      print('📡 Status Code: ${response.statusCode}');
      print('📡 Response Headers: ${response.headers}');
      print('📡 Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Verificar que los datos necesarios estén presentes
        if (data['access'] == null || data['usuario'] == null) {
          print('❌ Datos incompletos en respuesta');
          return LoginResult.error('Respuesta incompleta del servidor');
        }
        
        // Guardar tokens
        await StorageUtil.saveTokens(
          data['access'], 
          data['refresh']
        );
        
        // Guardar datos del usuario
        await StorageUtil.saveUserData(data['usuario']);
        
        // Actualizar estado
        _accessToken = data['access'];
        _currentUser = User.fromJson(data['usuario']);
        _isLoggedIn = true;
        
        notifyListeners();
        
        print('✅ Login exitoso para: ${_currentUser?.nombre} (${_currentUser?.rol})');
        return LoginResult.success('Login exitoso');
      } else {
        print('❌ Error HTTP ${response.statusCode}');
        try {
          final errorData = json.decode(response.body);
          return LoginResult.error(
            errorData['detail'] ?? errorData['error'] ?? 'Error del servidor'
          );
        } catch (e) {
          return LoginResult.error('Error del servidor (${response.statusCode})');
        }
      }
    } on SocketException catch (e) {
      print('💥 SocketException: $e');
      return LoginResult.error('No se puede conectar al servidor.\n\nVerifica que:\n• Django esté ejecutándose\n• Tu celular esté en Wi-Fi\n• La IP sea correcta (192.168.0.5)');
    } on TimeoutException catch (e) {
      print('💥 TimeoutException: $e');
      return LoginResult.error('Timeout de conexión.\nEl servidor no responde.');
    } on FormatException catch (e) {
      print('💥 FormatException: $e');
      return LoginResult.error('Error en formato de respuesta del servidor');
    } catch (e) {
      print('💥 Error general: $e');
      print('💥 Tipo: ${e.runtimeType}');
      return LoginResult.error('Error: ${e.toString()}');
    }
  }

  Future<void> logout() async {
    await StorageUtil.clearAll();
    _currentUser = null;
    _accessToken = null;
    _isLoggedIn = false;
    notifyListeners();
  }

  // Headers para requests autenticados
  Map<String, String> get authHeaders {
    return {
      'Content-Type': 'application/json',
      if (_accessToken != null) 'Authorization': 'Bearer $_accessToken',
    };
  }
}

class LoginResult {
  final bool isSuccess;
  final String message;

  LoginResult._(this.isSuccess, this.message);

  factory LoginResult.success(String message) => LoginResult._(true, message);
  factory LoginResult.error(String message) => LoginResult._(false, message);
}