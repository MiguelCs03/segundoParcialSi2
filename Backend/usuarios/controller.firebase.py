from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings
from .models import Usuario

# Inicializar Firebase con diccionario
if not firebase_admin._apps:
   try:
        firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if firebase_json:
            # ✅ Guardamos el contenido JSON temporalmente en un archivo
            with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_json:
                temp_json.write(firebase_json)
                temp_json.flush()
                cred = credentials.Certificate(temp_json.name)
                firebase_admin.initialize_app(cred)
        else:
            print("⚠️ No se encontró la variable FIREBASE_CREDENTIALS_JSON")
    except Exception as e:
        print(f"🔥 Error al inicializar Firebase: {e}")

def enviar_notificacion_firebase(titulo, mensaje, token):
    if not token or not isinstance(token, str):
        return {"enviado": False, "motivo": "Token inválido o vacío"}

    message = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje
        ),
        token=token
    )

    try:
        response = messaging.send(message)
        return {
            "enviado": True,
            "firebase_response": response
        }
    except Exception as e:
        return {"enviado": False, "motivo": f"Error al enviar: {e}"}

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def crear_notificacion_uni(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return Response(
            {"mensaje": "Usuario no encontrado"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data.copy()

    # Necesitas importar el serializer
        titulo = data.get("titulo", "Notificación")
        mensaje = data.get("mensaje", "")
        firebase_resultado = {"enviado": False, "motivo": ""}

        if usuario.fcm_token and usuario.fcm_token.strip():
            try:
                res = enviar_notificacion_firebase(titulo, mensaje, usuario.fcm_token)
                firebase_resultado = {
                    "enviado": res.get("enviado", False),
                    "motivo": res.get("motivo", "OK" if res.get("enviado") else "Sin motivo")
                }
            except Exception as e:
                firebase_resultado = {
                    "enviado": False,
                    "motivo": f"Error al enviar: {str(e)}"
                }
        else:
            firebase_resultado["motivo"] = "Usuario sin token FCM"

        return Response({
            "mensaje": "Notificación creada",
            "firebase": firebase_resultado
        }, status=status.HTTP_201_CREATED)

