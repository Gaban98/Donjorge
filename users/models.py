from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user (self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError('Debes tener un correo para completar el registro')
        if not username:
            raise ValueError('Debes tener un nombre de usuario para completar el registro')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_activate = True
        user.is_staff = True
        user.is_superuser = True #en el docuemto dice superadmin tenga cuidado#
        user.save(using=self._db)
        return user
    
class Users(AbstractBaseUser):

    ROLES = (
        ('admin', 'admin'),
        ('user', 'user'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(verbose_name='Correo electronico', max_length=60, unique=True)
    username = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=30, choices=ROLES, default='user')
    
    #required
    date_joined = models.DateTimeField(verbose_name='Fecha de creacion', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Ultimo inicio de sesion', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_activate = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) #en el documento sigue diciedno superadmin, cuidado#


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label): #en el documento dice add_label, cuidado#
        return True
    
    class Meta:
        verbose_name_plural = 'Usuarios'



