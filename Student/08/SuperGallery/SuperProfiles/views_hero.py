from pathlib import Path
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .views_functions import IsHeroCreatorMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Hero
from .views_reporter import get_reporter
    
class HeroListView(ListView):
    template_name = 'hero/list.html'
    model = Hero
    context_object_name = 'heroes'

    def get_context_data(self, **kwargs):
        return {
            'object_list': Hero.objects.all()
        }

class HeroDetailView(DetailView):
    template_name = 'hero/detail.html'
    model = Hero
    context_object_name = 'hero'

class HeroCreateView(LoginRequiredMixin, CreateView):
    template_name = "hero/add.html"
    model = Hero
    fields = '__all__'
    success_url = reverse_lazy('hero_list')

    def form_valid(self, form):
        form.instance.reporter = get_reporter(self.request.user)
        return super().form_valid(form)
    

class HeroUpdateView(IsHeroCreatorMixin, UpdateView):
    template_name = "hero/edit.html"
    model = Hero
    fields = '__all__'
    success_url = reverse_lazy('hero_list')

class HeroDeleteView(IsHeroCreatorMixin, DeleteView):
    template_name = 'hero/delete.html'
    model = Hero
    success_url = reverse_lazy('hero_list')