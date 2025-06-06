import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../constants/api_constants.dart';
import '../utils/storage.util.dart';

class NotificationService {
  static final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  static final FlutterLocalNotificationsPlugin _localNotifications = FlutterLocalNotificationsPlugin();
  
  static Future<void> initialize() async {
    try {
      // 🔥 Inicializar Firebase Core
      await Firebase.initializeApp(
        options: const FirebaseOptions(
          apiKey: 'AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  // Tu API Key
          appId: '1:123456789:android:abcdefxxxxxxxxxxxxxxxx',  // Tu App ID
          messagingSenderId: '123456789',  // Tu Sender ID
          projectId: 'colegio-cec69',  // Tu Project ID
        ),
      );
      print("✅ Firebase Core inicializado");
      
      // Solicitar permisos
      await _requestPermissions();
      
      // Configurar notificaciones locales
      await _initializeLocalNotifications();
      
      // Configurar handlers de Firebase
      _configureFirebaseHandlers();
      
      // Obtener y guardar token FCM
      await _getFCMToken();
      
    } catch (e) {
      print("❌ Error inicializando Firebase: $e");
    }
  }
  
  static Future<void> _requestPermissions() async {
    try {
      NotificationSettings settings = await _firebaseMessaging.requestPermission(
        alert: true,
        badge: true,
        sound: true,
        provisional: false,
      );
      
      print('📱 Permisos de notificación: ${settings.authorizationStatus}');
    } catch (e) {
      print('❌ Error solicitando permisos: $e');
    }
  }
  
  static Future<void> _initializeLocalNotifications() async {
    try {
      const AndroidInitializationSettings androidSettings = 
          AndroidInitializationSettings('@mipmap/ic_launcher');
      
      const DarwinInitializationSettings iosSettings = 
          DarwinInitializationSettings(
            requestAlertPermission: true,
            requestBadgePermission: true,
            requestSoundPermission: true,
          );
      
      const InitializationSettings settings = InitializationSettings(
        android: androidSettings,
        iOS: iosSettings,
      );
      
      await _localNotifications.initialize(
        settings,
        onDidReceiveNotificationResponse: (NotificationResponse response) {
          print('🔔 Notificación tocada: ${response.payload}');
        },
      );
      
      print("✅ Notificaciones locales inicializadas");
    } catch (e) {
      print('❌ Error inicializando notificaciones locales: $e');
    }
  }
  
  static void _configureFirebaseHandlers() {
    try {
      // Cuando la app está en foreground
      FirebaseMessaging.onMessage.listen((RemoteMessage message) {
        print('📨 Mensaje recibido en foreground: ${message.notification?.title}');
        _showLocalNotification(message);
      });
      
      // Cuando la app está en background y se toca la notificación
      FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
        print('📨 App abierta desde notificación: ${message.notification?.title}');
        _handleNotificationTap(message);
      });
      
      print("✅ Handlers de Firebase configurados");
    } catch (e) {
      print('❌ Error configurando handlers: $e');
    }
  }
  
  static Future<void> _showLocalNotification(RemoteMessage message) async {
    try {
      const AndroidNotificationDetails androidDetails = AndroidNotificationDetails(
        'aula_virtual_channel',
        'Aula Virtual',
        channelDescription: 'Notificaciones del aula virtual',
        importance: Importance.high,
        priority: Priority.high,
        showWhen: false,
      );
      
      const DarwinNotificationDetails iosDetails = DarwinNotificationDetails();
      
      const NotificationDetails details = NotificationDetails(
        android: androidDetails,
        iOS: iosDetails,
      );
      
      await _localNotifications.show(
        DateTime.now().millisecondsSinceEpoch ~/ 1000,
        message.notification?.title ?? 'Aula Virtual',
        message.notification?.body ?? 'Nueva notificación',
        details,
        payload: message.data.toString(),
      );
    } catch (e) {
      print('❌ Error mostrando notificación local: $e');
    }
  }
  
  static void _handleNotificationTap(RemoteMessage message) {
    print('🔔 Notification tapped: ${message.data}');
    // Aquí puedes navegar a una pantalla específica según el contenido
  }
  
  static Future<void> _getFCMToken() async {
    try {
      String? token = await _firebaseMessaging.getToken();
      if (token != null) {
        print('🔑 FCM Token obtenido: ${token.substring(0, 20)}...');
        await _sendTokenToServer(token);
      } else {
        print('❌ No se pudo obtener el FCM token');
      }
    } catch (e) {
      print('❌ Error obteniendo FCM token: $e');
    }
  }
  
  static Future<void> _sendTokenToServer(String token) async {
    try {
      final accessToken = await StorageUtil.getAccessToken();
      if (accessToken == null) {
        print('⚠️ No hay token de acceso, no se puede enviar FCM token');
        return;
      }
      
      final response = await http.post(
        Uri.parse('${ApiConstants.apiUrl}/usuario/fcm-token/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $accessToken',
        },
        body: json.encode({'fcm_token': token}),
      );
      
      if (response.statusCode == 200) {
        print('✅ FCM token enviado al servidor exitosamente');
      } else {
        print('❌ Error enviando FCM token: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('❌ Error enviando FCM token al servidor: $e');
    }
  }
  
  // Método para actualizar token cuando el usuario hace login
  static Future<void> updateTokenAfterLogin() async {
    try {
      await _getFCMToken();
    } catch (e) {
      print('❌ Error actualizando token después del login: $e');
    }
  }
}