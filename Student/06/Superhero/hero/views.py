from pathlib import Path
from typing import Any
from django import http
from django.views.generic import TemplateView

from .models import Superhero

class HeroView(TemplateView):
    template_name  = 'hero.html'

    def get_context_data(self, **kwargs):
        id = kwargs['pk']
        hero = Superhero.objects.get(pk=id)
        image = f'static\images\{hero.image}'
        return {'hero': hero,'image': image}
    

class HeroListView(TemplateView):
    template_name = 'heros.html'

    def get_context_data(self, **kwargs):
        heros = Superhero.objects.all()
        heros = [f for f in heros]
        return dict(heros=heros)  