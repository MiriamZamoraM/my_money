from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    Based on the UserManager of `django.contrib.auth.models`
    """

    user_in_migrations = True

    def create_user(self, email, password=None):

        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=False,
            is_superadmin=False,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=True,
            is_superadmin=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Correo electrónico", unique=True, blank=False)
    status_delete = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    intentos = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False, verbose_name="Es staff")
    is_superadmin = models.BooleanField(default=False, verbose_name="Es admin")
    is_superuser = models.BooleanField(default=False, verbose_name="Es super usuario")
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Usuario"

    def tokens_access(self):
        refresh = RefreshToken.for_user(self)
        return ({'access':str(refresh.access_token)})
 
    def tokens_refresh(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh':str(refresh)}