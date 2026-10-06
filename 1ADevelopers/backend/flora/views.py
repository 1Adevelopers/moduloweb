from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CategoriaEspecie, Especie, ImagenEspecie, Usuario
from .serializers import CategoriaSerializer, EspecieSerializer, ImagenEspecieSerializer


class Categorias(APIView):
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
    def get(self, request, pk):
        especie = get_object_or_404(Especie, pk=pk)
        serializer = EspecieSerializer(especie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        especie = get_object_or_404(Especie, pk=pk)
        serializer = EspecieSerializer (especie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        especie = get_object_or_404(Especie, pk=pk)
        especie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImagenEspecie(APIView):
    def get(self, request):
        ImagenEspecie = ImagenEspecie.objects.all()
        serializer = ImagenEspecieSerializer(ImagenEspecie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ImagenEspecieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        ImagenEspecie = get_object_or_404(ImagenEspecie, pk=pk)
        serializer = ImagenEspecieSerializer (ImagenEspecie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        ImagenEspecie = get_object_or_404(ImagenEspecie, pk=pk)
        ImagenEspecie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MisEspeciesListar(APIView):
    permission_classes = [IsAuthenticated] # cambio no subido aun, consultar con el equipo
    def get(self, request):
        usuario_id = request.query_params.get('usuario_id')

        if usuario_id:
            especies = Especie.objects.filter(usuario_id=usuario_id)
        else:
            return Response({"Error": "Falta el parámetro 'usuario_id'."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EspecieSerializer(especies, many=True)
        return Response(serializer.data)