from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


class AccountUserManager(BaseUserManager):
    def create_user(self,first_name, last_name, email, username, password):
        if not email:
            raise ValueError('this field cannot be empty')

        user= self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user=self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_superuser=True
        user.is_staff=True
        user.is_admin=True
        user.is_active=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=1500)
    phone_number = models.CharField (max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    created_date= models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)

    objects=AccountUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True
