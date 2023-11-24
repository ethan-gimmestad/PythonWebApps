from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Superhero
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, SuperheroForm  # Add SuperheroForm here
from django.contrib.auth.views import LoginView, LogoutView
from .mixins import AuthorRequiredMixin

class SuperheroListView(ListView):
    model = Superhero
    template_name = 'superheroes/superhero_list.html'

class SuperheroDetailView(DetailView):
    model = Superhero
    template_name = 'superheroes/superhero_detail.html'

class SuperheroCreateView(CreateView):
    model = Superhero
    form_class = SuperheroForm  # Specify your form class here
    template_name = 'your_template_name.html'  # Replace with your actual template name
    success_url = '/success/'  # Replace with your actual success URL

class SuperheroUpdateView(AuthorRequiredMixin, UpdateView):
    model = Superhero
    template_name = 'superheroes/superhero_form.html'
    fields = ['name', 'identity', 'description', 'strength', 'weakness', 'image']

class SuperheroDeleteView(DeleteView):
    model = Superhero
    template_name = 'superheroes/superhero_confirm_delete.html'
    success_url = reverse_lazy('superhero_list')

class UserLoginView(LoginView):
    template_name = 'superheroes/login.html'

class UserLogoutView(LogoutView):
    template_name = 'superheroes/logout.html'
