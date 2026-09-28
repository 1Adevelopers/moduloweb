from django.urls import path
from .views import (
    RolListarCrear,
    RolDetalle,
    UsuarioListarCrear,
    UsuarioDetalle,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path('roles/', RolListarCrear.as_view(), name='rol-listar-crear'),
    path('roles/<int:pk>/', RolDetalle.as_view(), name='rol-detalle'),

    path('usuarios/', UsuarioListarCrear.as_view(), name='usuario-listar'),
    path('usuarios/<int:pk>/', UsuarioDetalle.as_view(), name='usuario-detalle'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]