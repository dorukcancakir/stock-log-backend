from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from core.managers import UserManager
import core.enums as enums
from uuid import uuid4


def upload_to(instance, filename):
    folder = instance.__class__.__name__.lower()
    name = uuid4()
    extension = filename.split('.')[-1]
    return f'{folder}/{name}.{extension}'


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractBaseUser):
    company = models.ForeignKey(
        Company, related_name='users', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(
        max_length=10, choices=enums.Role.choices, default=enums.Role.USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['email']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['role']),
        ]


class ItemCategory(models.Model):
    company = models.ForeignKey(
        Company, related_name='item_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('company', 'name')
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['name']),
        ]


class Item(models.Model):
    company = models.ForeignKey(
        Company, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(
        ItemCategory, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveSmallIntegerField(default=1)
    min_quantity = models.PositiveSmallIntegerField(default=0)
    image = models.FileField(upload_to=upload_to)
    unit_of_measurement = models.CharField(
        max_length=10, choices=enums.Measurement.choices, default=enums.Measurement.PIECE)

    class Meta:
        unique_together = ('company', 'category', 'name')
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['category']),
            models.Index(fields=['name']),
            models.Index(fields=['quantity']),
            models.Index(fields=['min_quantity']),
        ]
