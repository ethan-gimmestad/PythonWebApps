from django.db import models
from django.contrib.auth.models import User

class Superhero(models.Model):
    name = models.CharField(max_length=200)
    identity = models.CharField(max_length=100, default='')
    description = models.TextField()
    strength = models.CharField(max_length=100, default='')
    weakness = models.CharField(max_length=100, default='')
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    bio = models.TextField()