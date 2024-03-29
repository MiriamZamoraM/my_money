from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, LoginSerializer, EmailVerificationSerializer, UserListSerializer


def send_user_mail(email, token):
    subject = "Your account needs to be verified"
    verification_link = f'http://127.0.0.1:8000/api/v1/users/verify/{token}'
    body = f'Hi, please click the following link to verify your account: \n {verification_link}'
    to = [email]

    message = EmailMultiAlternatives(subject, body, settings.EMAIL_HOST_USER, to)
    message.send()

class RegistryView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generar token JWT
            refresh_token = RefreshToken.for_user(user)
            token = str(refresh_token.access_token)

            # Enviar correo con el token generado
            send_user_mail(email=user.email, token=token)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
import jwt

class VerifyEmail(APIView):
    permission_classes = (AllowAny, )
    serializer_class = EmailVerificationSerializer

    def get(self, request, token):
        if token is None:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decodificar el token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            # Obtener el usuario asociado con el token
            user = User.objects.get(id=user_id)

            # Verificar si el usuario ya está verificado
            if user.is_verified:
                return Response({'message': 'User is already verified'}, status=status.HTTP_200_OK)

            # Activar la cuenta del usuario
            user.is_verified = True
            user.save()

            return Response({'message': 'User activated successfully'}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



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
        serializer = UserListSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)