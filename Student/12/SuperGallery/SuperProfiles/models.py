from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

def get_upload(instance, filename):
    return f'images/{filename}'

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
        return Hero.objects.filter(reporter=self)
    
    @property
    def photos(self):
        return Photo.objects.filter(reporter=self)

    @staticmethod
    def get_me(user):
        return Reporter.objects.get_or_create(user=user)[0]

class Photo (models.Model):

    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to=get_upload)

    def __str__(self):
        return f'{self.pk} - {self.title}'

    def get_absolute_url(self):
        return reverse_lazy('photo_detail', args=[str(self.id)])
    
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
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pk}. {self.title} - {self.realName}"
    
    @classmethod
    def create(cls, pk, reporter, photo, title, realName, strength1, strength2, strength3, weakness1, weakness2, weakness3, imagePath):
        hero = cls(pk=pk, reporter=reporter, photo=photo, title=title, realName=realName, strength1=strength1, strength2=strength2, strength3=strength3, weakness1=weakness1, weakness2=weakness2, weakness3=weakness3, imagePath=imagePath)
        return hero

class Article(models.Model):

    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, editable=False)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    body = models.TextField()
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pk}. {self.title} - {self.reporter.realName}"
    
    @classmethod
    def create(cls, pk, reporter, hero, title, tagline, body):
        article = cls(pk=pk, reporter=reporter, hero=hero, title=title, tagline=tagline, body=body)
        return article