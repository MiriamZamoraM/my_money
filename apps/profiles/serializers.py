from .models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'last_name', 'age', 'birthdate')

        def create(self, **validated_data):
            profile = Profile.objects.create(**validated_data)

            return profile