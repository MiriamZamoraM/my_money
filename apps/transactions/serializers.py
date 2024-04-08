from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Concept, Move, Color
from accounts.models import Account

class ConceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Concept
        fields = ('id', 'concept', 'type_movement', 'type_clasification', 'user', 'color', 'description')
    

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['color'] = ColorSerializer(instance.color.all(), many=True).data
        return response
        
#Serializer para listar gastos por color
class ConceptListSpentColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ['id', 'type_movement']
            
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['color'] = ColorSerializer(instance.color.all(), many=True).data
        return response


class MoveSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()
    class Meta:
        model = Move
        exclude = ('status_delete', )

    def create(self, validated_data):
        moves = Move.objects.create()
        moves.save()
        return moves

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['concept'] = ConceptSerializer(instance.concept.all(), many=True).data
        response['account'] = AccountBalanceSerializer(instance.account.all(), many=True).data
        return response

    
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Color
        exclude = ('status_delete', )


# Serializer para listar las cuentas de los movimientos.
class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Account
        fields = ['id', 'name']

# Serializer para listar los movimientos de los balances.
class BalanceMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ['name', 'day', 'amount', 'account', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['account'] = AccountBalanceSerializer(instance.account.all(), many=True).data
        return response

# Serializer para listar gastos por color
class MoveSpentColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        exclude = ('status_delete', )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['concept'] = ConceptSerializer(instance.concept.all(), many=True).data
        response['account'] = AccountBalanceSerializer(instance.account.all(), many=True).data
        return response
