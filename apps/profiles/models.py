from django.db import models
from users.models import User

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=150, verbose_name='Apellidos')
    age = models.IntegerField()
    birthdate = models.DateField(null= True, blank=True, verbose_name="Fecha de nacimiento")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'perfil'
        verbose_name = 'Perfil'