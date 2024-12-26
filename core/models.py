from django.db import models
import core.enums as enums
from uuid import uuid4
from django.contrib.auth.hashers import make_password, acheck_password, check_password


def upload_to(instance, filename):
    folder = instance.__class__.__name__.lower()
    name = uuid4()
    extension = filename.split('.')[-1]
    return f'{folder}/{name}.{extension}'


class CustomUserManager(models.Manager):
    def get_by_natural_key(self, email):
        return self.get(email=email)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]


class User(models.Model):
    company = models.ForeignKey(
        Company, related_name='users', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(
        max_length=10, choices=enums.Role.choices, default=enums.Role.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    async def set_password(self, raw_password):
        self.password = make_password(raw_password)
        await self.asave()

    async def acheck_password(self, raw_password):
        return await acheck_password(raw_password, self.password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return False

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['email']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]


class Inventory(models.Model):
    company = models.OneToOneField(
        Company, related_name='inventory', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory for {self.company.name}"

    class Meta:
        indexes = [
            models.Index(fields=['company']),
        ]


class ItemCategory(models.Model):
    company = models.ForeignKey(
        Company, related_name='item_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('company', 'name')
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['name']),
        ]


class ItemTag(models.Model):
    company = models.ForeignKey(
        Company, related_name='item_tags', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
    tag = models.ForeignKey(
        ItemTag, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to=upload_to, blank=True)
    unit_of_measurement = models.CharField(
        max_length=10, choices=enums.Measurement.choices, default=enums.Measurement.PIECE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('company', 'category', 'tag', 'name')
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['category']),
            models.Index(fields=['tag']),
            models.Index(fields=['name']),
        ]


class InventoryItem(models.Model):
    company = models.ForeignKey(
        Company, related_name='inventory_items', on_delete=models.CASCADE)
    inventory = models.ForeignKey(
        Inventory, related_name='inventory_items', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, related_name='inventory_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    min_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} in {self.inventory.company.name}"

    class Meta:
        unique_together = ('company', 'inventory', 'item')
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['inventory']),
            models.Index(fields=['item']),
            models.Index(fields=['quantity']),
            models.Index(fields=['min_quantity']),
        ]


class InventoryTransactionLog(models.Model):
    company = models.ForeignKey(
        Company, related_name='inventory_transaction_logs', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='inventory_transaction_logs', on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(
        InventoryItem, related_name='transaction_logs', on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10, choices=enums.TransactionType.choices)
    quantity = models.PositiveIntegerField(default=0)
    previous_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.inventory_item} by {self.user}"

    class Meta:
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['user']),
            models.Index(fields=['inventory_item']),
            models.Index(fields=['transaction_type']),
        ]
