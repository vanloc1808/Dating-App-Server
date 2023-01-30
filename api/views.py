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

from datetime import datetime
from api.utils import prime_number
from api.mail_handlers import forgot_password

# Create your views here.
class UserRegisterView(APIView):
    def post(self, request):
        request_data = request.data

        email = request_data.get('email')
        name = request_data.get('name')
        password = request_data.get('password')
        phone_number = request_data.get('phone_number')

        if email is None or name is None or password is None or phone_number is None:
            return JsonResponse({'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'message': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get the hash value of email using SHA256
        hash = sha256(email.encode('utf-8')).hexdigest()

        data_dict = {
            "hash_email": hash,
            "email": email,
            "name": name,
            "password": password,
            "phone_number": phone_number
        }

        answer_data_dict = {
            "hash_email": hash
        }

        serializer = UserSerializer(data=data_dict)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'message': 'successful', 'data': answer_data_dict}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)

        return JsonResponse({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginView(APIView):
    def post(self, request):
        request_data = request.data

        hash_email = request_data.get('hash_email')
        password = request_data.get('password')

        if hash_email is None or password is None:
            return JsonResponse({'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(hash_email=hash_email).exists():
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(hash_email=hash_email)
        if not user.password == password:
            return JsonResponse({'message': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'message': 'successful'}, status=status.HTTP_200_OK)

"""
    Password recovery code gotten by:
    a = month * day * hour * minute
    b = year * second
    min(a, b) <= p1, p2 <= max(a, b) with p1, p2 prime number
    recovery_key = (p1 * p2) % (10 ** 6)
"""
class UserPasswordForgotView(APIView):
    def post(self, request):
        request_data = request.data

        hash_email = request_data.get('hash_email')

        if hash_email is None:
            return JsonResponse({'message': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(hash_email=hash_email)
        # if user not exists
        if user is None:
            return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get the current date
        current_date = datetime.now()
        product1 = current_date.month * current_date.day * current_date.hour * current_date.minute
        product2 = current_date.year * current_date.second

        min_operand = min(product1, product2)
        max_operand = max(product1, product2)

        prime_list = prime_number.get_two_random_primes(min_operand, max_operand)
        
        recovery_key = (prime_list[0] * prime_list[1]) % (10 ** 6)

        str_recovery_key = str(recovery_key).zfill(6)

        forgot_password.send_password_recovery_mail(user.email, str_recovery_key)

        sha256_recovery_key = sha256(str_recovery_key.encode('utf-8')).hexdigest()

        return JsonResponse({'message': 'successful', 'data': {'sha256_recovery_key': sha256_recovery_key}}, status=status.HTTP_200_OK)