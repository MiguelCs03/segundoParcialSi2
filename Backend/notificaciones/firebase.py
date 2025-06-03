import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings

# Configuración de Firebase
FIREBASE_CONFIG = {
  "apiKey": "AIzaSyBdj6MtuiqYZDljJfss4KuiDQWRvqFONE8",
  "authDomain": "colegio-cec69.firebaseapp.com",
  "projectId": "colegio-cec69",
  "storageBucket": "colegio-cec69.firebasestorage.app",
  "messagingSenderId": "913551225849",
  "appId": "1:913551225849:web:6f832e42d19b5f9b7a0328"
}

# Inicializar Firebase Admin SDK
try:
    # Intentar inicializar con el archivo de credenciales
    cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
    
    if os.path.exists(cred_path):
        # Si el archivo existe, usarlo para la inicialización
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
        print("Firebase inicializado correctamente con credenciales")
    else:
        # Si no existe el archivo, usar inicialización simplificada
        print("Archivo de credenciales no encontrado, usando inicialización simplificada")
        firebase_app = firebase_admin.initialize_app()
        print("Firebase inicializado en modo simplificado")
        
except ValueError:
    # Si ya está inicializado
    firebase_app = firebase_admin.get_app()
    print("Firebase ya estaba inicializado")
except Exception as e:
    print(f"Error al inicializar Firebase: {e}")

def enviar_notificacion(token, titulo, mensaje, datos=None):
    """
    Envía una notificación push a un dispositivo específico
    """
    if datos is None:
        datos = {}
        
    mensaje_notificacion = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje,
        ),
        data=datos,
        token=token,
    )
    
    try:
        response = messaging.send(mensaje_notificacion)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

def enviar_notificacion_multiple(tokens, titulo, mensaje, datos=None):
    """
    Envía notificaciones push a múltiples dispositivos
    """
    if datos is None:
        datos = {}
        
    mensaje_multicast = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje,
        ),
        data=datos,
        tokens=tokens,
    )
    
    try:
        response = messaging.send_multicast(mensaje_multicast)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}