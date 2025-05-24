from django.urls import path
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from .views import UsuarioViewSet, login_view, logout_view, cambiar_contrasena
=======
from .views import UsuarioViewSet, LoginView, LogoutView, CambiarContrasenaView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
>>>>>>> backend_estructura

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
<<<<<<< HEAD
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cambiar-contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
]

urlpatterns += router.urls
=======
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cambiar-contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
]

urlpatterns += router.urls

urlpatterns += [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
>>>>>>> backend_estructura
