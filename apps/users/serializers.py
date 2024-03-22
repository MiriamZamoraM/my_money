from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)

    class Meta:
        model = User
        fields = ["email", "password", "name"]

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


# class UserLoginSerializar(serializers.ModelSerializer):
#     email = serializers.CharField(
#         required=True,
#     )
#     password = serializers.CharField(
#         required=True,
#     )
# 
#     class Meta:
#         model = User
#         fields = ("email", "password")