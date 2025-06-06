import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'core/services/auth_service.dart';
import 'core/services/notification_service.dart';  // 🔥 Agregar
import 'features/auth/views/login_screen.dart';
import 'features/profesor/views/profesor_dashboard.dart';
import 'features/estudiante/views/estudiante_dashboard.dart';
import 'features/tutor/views/tutor_dashboard.dart';
import 'shared/theme/app_theme.dart';

void main() async {
  // 🔥 Asegurar que Flutter esté inicializado
  WidgetsFlutterBinding.ensureInitialized();
  
  // 🔥 Inicializar Firebase y notificaciones
  try {
    await NotificationService.initialize();
    print("✅ Firebase y notificaciones inicializados");
  } catch (e) {
    print("❌ Error inicializando Firebase: $e");
  }
  
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) {
            final authService = AuthService();
            // 🔥 Inicializar el servicio de auth al crear
            authService.init();
            return authService;
          }
        ),
      ],
      child: Consumer<AuthService>(
        builder: (context, auth, _) {
          final router = GoRouter(
            initialLocation: '/',
            redirect: (context, state) {
              final isLoggedIn = auth.isLoggedIn;
              final isGoingToLogin = state.matchedLocation == '/login';
              
              // Si no está logueado y no va al login, redirigir al login
              if (!isLoggedIn && !isGoingToLogin) {
                return '/login';
              }
              
              // Si está logueado y va al login, redirigir al dashboard según rol
              if (isLoggedIn && isGoingToLogin) {
                return _getDashboardRoute(auth.userRole);
              }
              
              return null;
            },
            routes: [
              GoRoute(
                path: '/login',
                builder: (context, state) => LoginScreen(),
              ),
              GoRoute(
                path: '/',
                redirect: (context, state) => '/login',
              ),
              GoRoute(
                path: '/profesor',
                builder: (context, state) => ProfesorDashboard(),
              ),
              GoRoute(
                path: '/estudiante',
                builder: (context, state) => EstudianteDashboard(),
              ),
              GoRoute(
                path: '/tutor',
                builder: (context, state) => TutorDashboard(),
              ),
            ],
          );

          return MaterialApp.router(
            title: 'Aula Virtual',
            theme: AppTheme.lightTheme,
            routerConfig: router,
            debugShowCheckedModeBanner: false,
          );
        },
      ),
    );
  }

  String _getDashboardRoute(String? role) {
    switch (role?.toLowerCase()) {
      case 'profesor':
        return '/profesor';
      case 'estudiante':
        return '/estudiante';
      case 'tutor':
        return '/tutor';
      default:
        return '/login';
    }
  }
}
