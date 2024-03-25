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


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255, min_length = 3)
    password = serializers.CharField(max_length = 150, min_length = 6, write_only = True)
    name = serializers.CharField(max_length = 255, min_length = 3, read_only = True)
    

    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'tokens_refresh', 'tokens_access']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user_email = User.objects.get(email = email)
        user = auth.authenticate(email = email, password = password)

        if user_email.intentos < 3:
            while not user:
                user_email.intentos += 1
                user_email.save()
                raise AuthenticationFailed({'isAuthorized' : 'false'})
        else:
            user_email.is_active = False
            user_email.save() 
            raise AuthenticationFailed({'isAuthorized' : 'false'})

        if user:
            user.intentos = 0
            user.save()
                 

        return{
            'email': user.email,
            'name' : user.name,
            'tokens_access' : user.tokens_access(),
            'tokens_refresh' : user.tokens_refresh(),

        } 
        return attrs
        