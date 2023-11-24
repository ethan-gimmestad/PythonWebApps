# superheroes/models.py

from django.db import models

class Superhero(models.Model):
    name = models.CharField(max_length=255)
    identity = models.CharField(max_length=255)
    description = models.TextField()
    strength = models.CharField(max_length=255)
    weakness = models.CharField(max_length=255)
    image = models.ImageField(upload_to='superheroes/images/')

    def __str__(self):
        return self.name
