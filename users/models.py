from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import UserManager

""" class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields) """

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return str(self.email)
    

class Student(User):
    group_number = models.CharField(max_length=20, blank=True, null=True)
    direction_of_training = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'student'
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

class Teacher(User):
    post = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    

