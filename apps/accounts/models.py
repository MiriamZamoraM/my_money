from django.db import models
from users.models import User

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nombre')
    type_opc = [
		('ahorro','Ahorro'),
		('nomina','Nómina'),
		('efectivo','Efectivo'),
		('inversion','Inversión'),
		('credito','Crédito'),
		('wallet','Wallet'),
		('departamental','Departamental'),
        ('vales','Vales')
    ]
    type_account = models.CharField(choices=type_opc, max_length=50, verbose_name='Tipo de cuenta')
    public_key = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name='Cuenta pública')
    number = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='Número')
    cvv = models.CharField(max_length=3, blank=True, verbose_name= 'CVV')
    balance = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Saldo')
    due_date = models.DateField(null= True, blank=True, verbose_name="Fecha de corte")
    is_active = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status_delete = models.BooleanField(default=False)


    class Meta:
            db_table = 'accounts'