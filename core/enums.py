from django.db.models import TextChoices
from strawberry import enum


@enum
class TransactionType(TextChoices):
    NEW_ITEM = 'NEW_ITEM'
    INCREASE = 'INCREASE'
    DECREASE = 'DECREASE'


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
