from rest_framework import serializers
from users.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)

    class Meta:
        model = User
        fields = ["id", "email", "password", "name"]

    def create(self, validated_data):
        model = self.Meta.model
        password = validated_data["password"]
        email = validated_data["email"]
        name = validated_data["name"]

        user = model.objects.create(email=email)
        user.set_password(password)
        user.save()

        return user

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.email,
        }

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "is_verified"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.email,
            "is_verified":instance.is_verified,
        }

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)

    class Meta:
        model = User
        fields = ['token']

from rest_framework.exceptions import AuthenticationFailed

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=150, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'tokens_refresh', 'tokens_access']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        try:
            # Obtener el usuario por correo electrónico
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Manejar el caso donde el usuario no existe
            raise AuthenticationFailed('User not found')

        # Verificar si la cuenta está bloqueada
        if user.intentos >= 3:
            user.is_active = False
            user.save()
            raise AuthenticationFailed('Account is locked')

        # Autenticar al usuario
        if not user.check_password(password):
            # Actualizar los intentos del usuario si las credenciales son inválidas
            user.intentos += 1
            user.save()
            raise AuthenticationFailed('Invalid credentials')

        # Reiniciar los intentos si las credenciales son válidas
        user.intentos = 0
        user.save()

        return {
            'email': user.email,
            'tokens_access': user.tokens_access(),
            'tokens_refresh': user.tokens_refresh(),
        }

        