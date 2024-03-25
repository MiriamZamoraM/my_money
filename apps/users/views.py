import email
import jwt
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import EmailMultiAlternatives

def send_user_mail(email, token):
    # user=User.objects.filter(email=email)

    token = RefreshToken.for_user(User).access_token
    subject="Your account needs to be verified"
    body=f'Hi paste your link to verify your account http://127.0.0.1:8000/api/v1/users/verify/{token}'
    to=[email]

    message = EmailMultiAlternatives(subject, body, settings.EMAIL_HOST_USER, to)
    message.send()

class RegistryView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.last()
            send_user_mail(user, id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
class VerifyEmail(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def get(self, request, token):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verify:
                user.is_verify = True
                user.save()
            return Response({'email' : 'Successfully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error' : 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return Response({'error' : 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception = True)

            return Response(serializer.data, status=status.HTTP_200_OK)


class ListApiView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request):
        users_list = User.objects.all().filter(status_delete=False)
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)