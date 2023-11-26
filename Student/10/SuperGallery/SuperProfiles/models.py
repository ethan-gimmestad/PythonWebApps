from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class Reporter(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)

    realName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse_lazy('reporter_detail', args=[str(self.id)])

    @property
    def name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def heroes(self):
        return Hero.objects.filter(author=self)

    @staticmethod
    def get_me(user):
        return Reporter.objects.get_or_create(user=user)[0]

class Hero(models.Model):

    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, editable=False)

    title = models.CharField(max_length=100)
    realName = models.CharField(max_length=100)
    strength1 = models.CharField(max_length=200)
    strength2 = models.CharField(max_length=200)
    strength3 = models.CharField(max_length=200)
    weakness1 = models.CharField(max_length=200)
    weakness2 = models.CharField(max_length=200)
    weakness3 = models.CharField(max_length=200)
    imagePath = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.pk}. {self.title} - {self.realName}"
    
class Article(models.Model):

    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, editable=False)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    body = models.TextField()

    @property
    def imagePath(self):
        return self.hero.imagePath

    def __str__(self):
        return f"{self.pk}. {self.title} - {self.reporter.realName}"