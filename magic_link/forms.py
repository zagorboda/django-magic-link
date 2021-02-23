from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        print(self.cleaned_data)
        print(self.cleaned_data['email'])
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            raise forms.ValidationError("A user with that email already exists.")


class LoginForm(forms.Form):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=100)
