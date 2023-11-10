from pathlib import Path
from typing import Any
from django import http
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Superhero
from django.views.generic import CreateView
from django.views.generic import RedirectView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic import DetailView

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
    



class UserAddView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



class UserHomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return '/article/'
        return f'/author/{get_me(self.request.user).pk}'

def get_me(user):
    return Author.objects.get_or_create(user=user)[0]

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "account_edit.html"
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    success_url = reverse_lazy('home')

class AuthorDetailView(DetailView):
    template_name = 'author_detail.html'
    model = Author