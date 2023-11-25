from django.db import models

class Superhero(models.Model):
    name = models.CharField(max_length=255, unique=True)
    powers = models.TextField()
    origin = models.TextField()

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add any additional user fields here
    pass
