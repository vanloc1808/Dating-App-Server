from django.shortcuts import render
from django.http import JsonResponse


from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from api.models import User
from api.serializers import UserSerializer
from hashlib import sha256
from rest_framework.views import APIView

# Create your views here.
class UserRegisterView(APIView):
    def post(self, request):
        request_data = request.data

        email = request_data.get('email')
        print("Email", email)
        name = request_data.get('name')
        password = request_data.get('password')
        phone_number = request_data.get('phone_number')
        print(len(password))

        if email is None or name is None or password is None or phone_number is None:
            return JsonResponse({'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get the hash value of email using SHA256
        hash = sha256(email.encode('utf-8')).hexdigest()

        data_dict = {
            "hash_email": hash,
            "email": email,
            "name": name,
            "password": password,
            "phone_number": phone_number
        }

        serializer = UserSerializer(data=data_dict)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'message': 'successful', 'data': data_dict}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)

        return JsonResponse({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)