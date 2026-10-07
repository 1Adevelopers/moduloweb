from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Contacto
from .serializers import ContactoSerializer


class ContactoListarCrear(APIView):
   def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]
       
   def get(self, request):
       contactos = Contacto.objects.all()
       serializer = ContactoSerializer(contactos, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)


   def post(self, request):
       serializer = ContactoSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactoDetalle(APIView):
    permission_classes = [IsAuthenticated]

   
    def get(self, request, pk):
       contacto = get_object_or_404(Contacto, pk=pk)
       serializer = ContactoSerializer(contacto)
       return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
       contacto = get_object_or_404(Contacto, pk=pk)
       serializer = ContactoSerializer(contacto, data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
       contacto = get_object_or_404(Contacto, pk=pk)
       contacto.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)
   
class ContactoMarcarLeido(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        contacto = get_object_or_404(Contacto, pk=pk)
        contacto.leido = True
        contacto.save()
        serializer = ContactoSerializer(contacto)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactoMarcarRespondido(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        contacto = get_object_or_404(Contacto, pk=pk)
        contacto.respondido = True
        contacto.save()
        serializer = ContactoSerializer(contacto)
        return Response(serializer.data, status=status.HTTP_200_OK)