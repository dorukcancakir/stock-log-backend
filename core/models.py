from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from core.managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    objects = UserManager()
    USERNAME_FIELD = 'email'
