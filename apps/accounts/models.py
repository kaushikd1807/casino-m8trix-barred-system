from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPE_CHOICES = (('security', 'security'),
                    ('security_supervisor', 'security_supervisor'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='security')

    def __str__(self):
        return self.username
