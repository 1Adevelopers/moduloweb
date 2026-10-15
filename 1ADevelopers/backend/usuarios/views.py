import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Rol, Usuario
from .serializers import RolSerializer, UsuarioSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

logger = logging.getLogger('seguridad')
ID_ROL_ADMIN = 1

class RolListarCrear(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolDetalle(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        roles = get_object_or_404(Rol, pk=pk)
        serializer = RolSerializer(roles)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        roles = get_object_or_404(Rol, pk=pk)
        serializer = RolSerializer(roles, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        roles = get_object_or_404(Rol, pk=pk)
        roles.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsuarioListarCrear(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetalle(APIView):
    permission_classes = [IsAuthenticated]

    def _es_admin(self, request):
        return getattr(request.user, 'rol_id', None) == ID_ROL_ADMIN

    def _obtener_usuario_permitido(self, request, pk, solo_admin=False):
        """Devuelve el usuario solo si quien consulta es el mismo usuario o un administrador."""
        usuario = get_object_or_404(Usuario, pk=pk)
        es_admin = self._es_admin(request)
        es_el_mismo = getattr(request.user, 'id', None) == usuario.id

        if es_admin or (es_el_mismo and not solo_admin):
            return usuario

        logger.warning(
            f"Acceso denegado: el usuario {getattr(request.user, 'id', None)} intentó "
            f"{request.method} sobre el usuario {pk}"
        )
        raise PermissionDenied('No tiene permiso para acceder a este usuario.')

    def get(self, request, pk):
        usuario = self._obtener_usuario_permitido(request, pk)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        usuario = self._obtener_usuario_permitido(request, pk)
        serializer = UsuarioSerializer(usuario, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        usuario = self._obtener_usuario_permitido(request, pk, solo_admin=True)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        contrasena = request.data.get('contrasena')

        if not email or not contrasena:
            return Response(
                {'error': 'Faltan datos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = Usuario.objects.get(email=email, contrasena=contrasena)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Email o contraseña incorrectos'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenRefreshSerializer



          
            
            