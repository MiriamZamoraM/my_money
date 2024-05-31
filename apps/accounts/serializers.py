from rest_framework import serializers
from .models import Account

from django.forms import DateInput, ValidationError

class AccSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('status_delete','is_active',)

    def validate(self,attrs):

        tipo = attrs.get('type_account')
        wallet = attrs.get('public_key', None)
        
        if tipo == 'wallet':
            wallet = attrs.get('public_key', None)
            if wallet is None:
                raise ValidationError('El campo cuenta pública es requerido')
            
        elif tipo == 'credito':
            credito = attrs.get('due_date', None)
            if credito is None:
                raise ValidationError('El campo fecha de corte es requerido')
        elif tipo != 'efectivo' and tipo != 'wallet':
            numero_cuenta = attrs.get('number', None)
            if numero_cuenta is None:
                raise ValidationError('El campo Número de cuenta es requerido')
            codigo = attrs.get('cvv', None)
            if codigo is None:
                raise ValidationError('El campo CVV es requerido')
        return attrs
    
    def create(self, validated_data):

        account = Account.objects.create(**validated_data)

        return account