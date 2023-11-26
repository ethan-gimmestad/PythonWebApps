from pathlib import Path
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, RedirectView

from .models import Hero, Reporter
    
def list_heroes(reporter):
    return dict(heroes=Hero.objects.filter(reporter=reporter))


def get_reporter(user):
    return Reporter.objects.get_or_create(user=user)[0]


class ReporterAddView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/account_add.html'

class ReporterHomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return '/hero/'
        return f'/reporter/{get_reporter(self.request.user).pk}'
    
class ReporterListView(ListView):
    template_name = 'reporter/list.html'
    model = Reporter

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        return kwargs


class ReporterDetailView(DetailView):
    template_name = 'reporter/detail.html'
    model = Reporter

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(list_heroes(kwargs.get('object')))
        return kwargs


class ReporterUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "reporter/edit.html"
    model = Reporter
    fields = '__all__'
    success_url = reverse_lazy('reporter_list')