from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from .models import CategoriaEspecie, Especie, ImagenEspecie, Usuario
from .serializers import CategoriaSerializer, EspecieSerializer, ImagenEspecieSerializer
from usuarios.models import Usuario

def obtener_usuario_desde_token(request):
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        raw_token = auth_header.split(' ')[1]
        try:
            access_token = AccessToken(raw_token)
            user_id = access_token.get('user_id')
            return Usuario.objects.get(id=user_id)
        except Exception:
            return None
    return None

class Categorias(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request):
        categorias = CategoriaEspecie.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        categoria = get_object_or_404(CategoriaEspecie, pk=pk)
        serializer = CategoriaSerializer (categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        categoria = get_object_or_404(Categorias, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class EspecieListarCrear(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        especies = Especie.objects.all()
        serializer = EspecieSerializer(especies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EspecieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EspecieDetalle(APIView):
    def get_permissions(self):
            if self.request.method == 'GET':
                return [AllowAny()]
            return [IsAuthenticated()]

    def get(self, request, pk):
        especie = get_object_or_404(Especie, pk=pk)
        serializer = EspecieSerializer(especie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        especie = get_object_or_404(Especie, pk=pk)
        serializer = EspecieSerializer(especie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        especie = get_object_or_404(Especie, pk=pk)
        especie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImagenEspecie(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        imagenes = ImagenEspecie.objects.all()
        serializer = ImagenEspecieSerializer(imagenes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ImagenEspecieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        imagen = get_object_or_404(ImagenEspecie, pk=pk)
        serializer = ImagenEspecieSerializer(imagen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        imagen = get_object_or_404(ImagenEspecie, pk=pk)
        imagen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MisEspeciesListar(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        usuario_logueado = obtener_usuario_desde_token(request)
        
        if usuario_logueado:
            especies = Especie.objects.filter(usuario=usuario_logueado)
        else:
            usuario_id = request.query_params.get('usuario_id')
            if usuario_id:
                especies = Especie.objects.filter(usuario_id=usuario_id)
            else:
                return Response({"Error": "No autenticado o falta el parámetro 'usuario_id'."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = EspecieSerializer(especies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

