import logging
import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Rol, Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('seguridad')

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre_rol']

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, write_only=True)
    password = serializers.CharField(write_only=True)
    contrasena = serializers.CharField(required=False, write_only=True)
    
    def validate(self, attrs):
        
        email = attrs.get('email')
        pass_usuario = attrs.get('contrasena') or attrs.get('password')
        
        if not email or not pass_usuario:
            raise serializers.ValidationError('Se requiere email y contraseña')
        
                
        user = Usuario.objects.filter(email=email).first()
        if user is None or not check_password(pass_usuario, user.contrasena):
            logger.warning(f"Intento de acceso denegado (Login fallido). Email usado: {email}")
            raise serializers.ValidationError('Credenciales incorrectas')    

        refresh = RefreshToken()
        refresh['user_id'] = user.id        
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'nombre': user.nombre,
                'apellido': user.apellido,
                'email': user.email,
                'rol': user.rol.id
            }
            }


class UsuarioSerializer(serializers.ModelSerializer):

    rol_nombre = serializers.ReadOnlyField(source='rol.nombre_rol')

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'email', 'rol', 'rol_nombre', 'contrasena']
        # agrege contrasena en fields| Se proteje para que la contraseña no se envíe al frontend
        read_only_fields = ['id', 'rol_nombre']
        extra_kwargs = {
            'contrasena': {'write_only': True, 'required':False},
            'rol': {'required': False}
        }

        
    def validate_contrasena(self, value):
        """Política de contraseñas: mínimo 8 caracteres, con mayúscula, minúscula y número."""
        if not value:
            return value
        errores = []
        if len(value) < 8:
            errores.append('Debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', value):
            errores.append('Debe incluir al menos una letra mayúscula.')
        if not re.search(r'[a-z]', value):
            errores.append('Debe incluir al menos una letra minúscula.')
        if not re.search(r'\d', value):
            errores.append('Debe incluir al menos un número.')
        if errores:
            raise serializers.ValidationError(errores)
        return value
    
    def create(self, validated_data):
        if not validated_data.get('contrasena'):
            raise serializers.ValidationError({'contrasena': 'La contraseña es obligatoria para registrar un nuevo usuario'})
        
        rol_data = validated_data.pop('rol', None)
        
        es_admin = self._verificar_si_es_admin()

        if es_admin and rol_data:
            if isinstance(rol_data, dict):
                validated_data['rol_id'] = rol_data.get('id', 2)
            else:
                validated_data['rol'] = rol_data
        else:
            validated_data['rol_id'] = 2
            validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return Usuario.objects.create(**validated_data)

        return Usuario.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('email', instance.email)
        
        nueva_contrasena = validated_data.get('contrasena')
        if nueva_contrasena:
            instance.contrasena = make_password(nueva_contrasena)

        if 'rol' in validated_data:
            es_admin = self._verificar_si_es_admin()
            if es_admin:
                instance.rol = validated_data.get('rol')
            else:
                validated_data.pop('rol', None)

        instance.save()
        return instance

    def _verificar_si_es_admin(self):
        request = self.context.get('request')
        if not request:
            return False

        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            raw_token = auth_header.split(' ')[1]
            try:
                access_token = AccessToken(raw_token)
                user_id = access_token.get('user_id')
                if not user_id:
                    return False
                
                usuario_logueado = Usuario.objects.get(id=user_id)
                return usuario_logueado.rol.id == 1
            except Exception:
                return False
        return False


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            return Usuario.objects.get(id=user_id)
        except (KeyError, Usuario.DoesNotExist):
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed('User not found', code='user_not_found')