from rest_framework import serializers
from .models import Rol, Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre_rol']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=False, write_only=True)
    email = serializers.EmailField(required=False, write_only=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        
        identificador = attrs.get('email') or attrs.get('username')
        password = attrs.get('password')
        
        if not identificador or not password:
            raise serializers.ValidationError('Se requiere email/username y contraseña')
        
        try:
            user = Usuario.objects.get(email=identificador, contrasena=password)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Credenciales inválidas')    
  
  
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

        return Usuario.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('email', instance.email)
        
        nueva_contrasena = validated_data.get('contrasena')
        if nueva_contrasena:
            instance.contrasena = nueva_contrasena

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
                
                usuario_logueado = Usuario.objects.get(id=user_id)
                return usuario_logueado.rol.id == 1
            except Exception:
                return False
        return False