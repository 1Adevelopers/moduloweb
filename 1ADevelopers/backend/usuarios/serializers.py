from rest_framework import serializers
from .models import Rol, Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
  
  
        refresh = RefreshToken.for_user(user)        
        
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
        extra_kwargs = {
            'contrasena': {'write_only': True, 'required':False},
            'rol': {'required': False}
        }
    
    def create(self, validated_data):
        if not validated_data.get('contrasena'):
            raise serializers.ValidationError({'contrasena': 'La contraseña es obligatoria para registrar un nuevo usuario'})
        
        rol_data = validated_data.pop('rol', None)
        
        # Si no viene rol (registro público), asignamos el ID 2 directamente
        if not rol_data:
            validated_data['rol_id'] = 2
        # Si viene como diccionario (desde alguna otra vista)
        elif isinstance(rol_data, dict):
            validated_data['rol_id'] = rol_data.get('id', 2)
        # Si ya es una instancia del modelo Rol (comportamiento por defecto de DRF)
        else:
            validated_data['rol'] = rol_data
            
        return Usuario.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('email', instance.email)
        
        nueva_contrasena = validated_data.get('contrasena')
        if nueva_contrasena:
            instance.contrasena = nueva_contrasena
        
        if 'rol' in validated_data:
            instance.rol = validated_data.get('rol')
            
        instance.save()
        return instance