from django import forms
from .models import Superhero
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SuperheroForm(forms.ModelForm):  # Add this form for Superhero model
    class Meta:
        model = Superhero
        fields = '__all__'  # You can customize this based on the fields you want in your form
