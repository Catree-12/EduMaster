from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,CustomTokenObtainPairSerializer
from rest_framework import status   

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
# Create your views here.
from rest_framework.permissions import AllowAny

class User_register(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
   
    
    def post(self, request, format=None):
        
        serializer = self.get_serializer(data=request.data)   
        if serializer.is_valid(raise_exception=True):
            a=serializer.save()
            return Response({'message': '欢迎.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User_login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def get(self, request, *args, **kwargs):
        return Response({'message': '欢迎宝贝.'}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


            

