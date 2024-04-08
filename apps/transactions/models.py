from django.db import models
from accounts.models import Account
from users.models import User

# Create your models here.

# Éste es el modelo de Recursos.
class Color(models.Model):
        type_color = [
            ('#FF6900','Naranja'),
            ('#FCB900','Amarillo'),
            ('#7BDCB5', 'Turquesa'),
            ('#00D084', 'Verde'),
            ('#8ED1FC', 'Azul cielo'),
            ('#0693E3', 'Azul'),
            ('#ABB8C3', 'Verde limón'),
            ('#EB144C', 'Rosa mexicano'),
            ('#F78DA7', 'Rosa claro'),
            ('#9900EF', 'Morado')

        ]
        color = models.CharField(choices=type_color, max_length=30, default='#E9E9E9', verbose_name='Color')
        status_delete = models.BooleanField(default=False)

        class Meta:
            db_table= 'colors'

# Éste es el modelo de Conceptos.
class Concept(models.Model):

    concept = models.CharField(max_length=200, verbose_name='Concepto')
    description = models.CharField(max_length=200, blank=True, verbose_name= 'Descripcion del concepto')
    type_mov = [
        ('gasto','Gasto'),
        ('ingreso','Ingreso')
     ]
    type_movement = models.CharField(choices=type_mov, max_length=10, verbose_name='Tipo de movimiento')
    type_clasif = [
        ('fijo','Fijo'),
        ('variable','Variable')
    ]
    type_clasification = models.CharField(choices=type_clasif, max_length=10, verbose_name='Tipo de clasificación')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status_delete = models.BooleanField(default=False)
    color = models.ManyToManyField(Color, default=1)

    class Meta:
        db_table = 'concepts'

# Éste es el modelo de Movimientos.
class Move(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre del movimiento')
    description = models.CharField(max_length=200, blank=True, verbose_name= 'Descripcion del movimiento')
    day = models.DateField(verbose_name='Dia del movimiento')
    amount = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Importe del movimiento')
    picture = models.ImageField(upload_to="movimientos", default="image.jpg")
    account = models.ManyToManyField(Account)
    concept = models.ManyToManyField(Concept)
    status_delete = models.BooleanField(default=False)

    class Meta:
        db_table= 'moves' 
