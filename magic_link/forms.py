from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class LoginForm(forms.Form):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=100)
