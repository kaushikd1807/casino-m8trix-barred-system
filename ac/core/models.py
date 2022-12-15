import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Brokerage(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=200, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=50, blank=True)
    logo = models.FileField(upload_to="documents/logos", null=True, blank=True)


# Custom User Model
TYPE_CHOICES = (('customer', 'customer'),
                ('agent', 'agent'))

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.EmailField(max_length=255, unique=True)
    brokerage = models.ForeignKey(
        Brokerage, 
        null=True, blank=True, 
        on_delete=models.SET_NULL,
        related_name="agents"
        )
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_photo = models.FileField(upload_to="documents/profiles/", null=True, blank=True)
    user_type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='agent')
    bio = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.username)


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "countries"
        verbose_name_plural = "Manage Countries"

    def __str__(self):
        return '{}'.format(self.name)
