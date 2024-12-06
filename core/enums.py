from django.db.models import TextChoices
from strawberry import enum


@enum
class Measurement(TextChoices):
    PIECE = 'PIECE'
    LITRE = 'LITRE'
    KILOGRAM = 'KILOGRAM'
    METER = 'METER'


@enum
class Role(TextChoices):
    ADMIN = 'ADMIN'
    USER = 'USER'
