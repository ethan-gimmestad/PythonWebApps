from json import loads
from pathlib import Path
from django.contrib.auth.mixins import AccessMixin
from .models import Hero, Article, Reporter
from django.shortcuts import get_object_or_404
from markdown import markdown
from django.core.management import call_command
from django.http import HttpResponse
import subprocess
from csv import reader, writer

class IsHeroCreatorMixin(AccessMixin):
    def test_func(self):
        hero = get_object_or_404(Hero, pk = self.kwargs["pk"])
        return self.request.user == hero.reporter.user

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
class IsArticleCreatorMixin(AccessMixin):
    def test_func(self):
        article = get_object_or_404(Article, pk = self.kwargs["pk"])
        return self.request.user == article.reporter.user

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def document_card(document):
    d = f'documents/{document}'
    if not d.endswith('.md'):
        d = d + '.md'
    markdown_text = open(d).read()
    return dict(body=markdown(markdown_text), file=document, color='bg-primary text-light p-5', width='')

def card_data(title=None, body=None, link=None, imagePath=None, tagline=None, realName=None, strength1=None, strength2=None, strength3=None, weakness1=None, weakness2=None, weakness3=None):
    return dict(title=title, header=title, body=body, link=link, imagePath=imagePath, tagline=tagline, realName=realName, strength1=strength1, strength2=strength2, strength3=strength3, weakness1=weakness1, weakness2=weakness2, weakness3=weakness3)

def exportArticleJSONData(request):
    output_data = subprocess.check_output(['python', 'manage.py', 'dumpdata', 'SuperProfiles.Article', '--indent', '2'])
    output_data = output_data.decode("latin-1")
    with open("articleJSONData.json", "w") as file:
        file.write(output_data)
    return HttpResponse("Data Exported!")

def loadArticleJSONData(request):
    call_command('loaddata', 'articleJSONData.json')
    return HttpResponse("File Loaded!")

def exportArticleCSVData(request):
    table = [[a.pk, a.reporter.pk, a.hero.pk, a.title, a.tagline, a.body] for a in Article.objects.all()]
    with open("articleCSVData.csv", 'w', newline='') as f:
        writer(f).writerows(table)
    return HttpResponse("Data Exported!")

def loadArticleCSVData(request):
    with open("articleCSVData.csv") as f:
        for row in reader(f):
            reporter = get_object_or_404(Reporter, pk = row[1])
            hero = get_object_or_404(Hero, pk = row[2])
            article = Article.create(row[0], reporter, hero, row[3], row[4], row[5])
            article.save()
    return HttpResponse("File Loaded!")

def exportHeroJSONData(request):
    output_data = subprocess.check_output(['python', 'manage.py', 'dumpdata', 'SuperProfiles.Hero', '--indent', '2'])
    output_data = output_data.decode("utf-8")
    with open("heroJSONData.json", "w") as file:
        file.write(output_data)
    return HttpResponse("Data Exported!")

def loadHeroJSONData(request):
    call_command('loaddata', 'heroJSONData.json')
    return HttpResponse("File Loaded!")

def exportHeroCSVData(request):
    table = [[h.pk, h.reporter.pk, h.title, h.realName, h.strength1, h.strength2, h.strength3, h.weakness1, h.weakness2, h.weakness3, h.imagePath] for h in Hero.objects.all()]
    with open("heroCSVData.csv", 'w', newline='') as f:
        writer(f).writerows(table)
    return HttpResponse("Data Exported!")

def loadHeroCSVData(request):
    with open("heroCSVData.csv") as f:
        for row in reader(f):
            reporter = get_object_or_404(Reporter, pk = row[1])
            hero = Hero.create(row[0], reporter, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            hero.save()
    return HttpResponse("File Loaded!")
